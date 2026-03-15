"""Script mínimo para fazer upload de um arquivo para um bucket no GCS."""

import os
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import storage


load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
LOCAL_FILE_PATH = os.getenv("LOCAL_FILE_PATH")
DESTINATION_BLOB_NAME = os.getenv("DESTINATION_BLOB_NAME")

if not PROJECT_ID:
    raise ValueError("Defina GCP_PROJECT_ID no arquivo .env")
if not BUCKET_NAME:
    raise ValueError("Defina GCS_BUCKET_NAME no arquivo .env")
if not LOCAL_FILE_PATH:
    raise ValueError("Defina LOCAL_FILE_PATH no arquivo .env")

local_file = Path(LOCAL_FILE_PATH)
if not local_file.exists() or not local_file.is_file():
    raise FileNotFoundError(f"Arquivo não encontrado: {local_file}")

blob_name = DESTINATION_BLOB_NAME or local_file.name

client = storage.Client(project=PROJECT_ID)
bucket = client.lookup_bucket(BUCKET_NAME)
if not bucket:
    raise ValueError(f"Bucket não existe ou sem acesso: {BUCKET_NAME}")

blob = bucket.blob(blob_name)
blob.upload_from_filename(str(local_file))

print(f"Upload concluído: {local_file} -> gs://{BUCKET_NAME}/{blob_name}")
