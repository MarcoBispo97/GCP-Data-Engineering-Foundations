"""Script mínimo para criar um bucket no Google Cloud Storage."""

import os

from dotenv import load_dotenv
from google.cloud import storage


load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")

if not PROJECT_ID:
    raise ValueError("Defina GCP_PROJECT_ID no arquivo .env")
if not BUCKET_NAME:
    raise ValueError("Defina GCS_BUCKET_NAME no arquivo .env")

client = storage.Client(project=PROJECT_ID)

bucket = client.lookup_bucket(BUCKET_NAME)
if bucket:
    print(f"Bucket já existe: {BUCKET_NAME}")
else:
    bucket = client.bucket(BUCKET_NAME)
    client.create_bucket(bucket, location="US")
    print(f"Bucket criado com sucesso: {BUCKET_NAME}")
