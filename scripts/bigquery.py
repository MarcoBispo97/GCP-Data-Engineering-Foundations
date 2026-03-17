from google.cloud import storage
from google.api_core.exceptions import Conflict
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

service_account_json_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
project_id = os.getenv("GCP_PROJECT_ID", "global-grammar-432121-d7")
bucket_name = "my_test_bucket_name_12345"  # Change to a unique bucket name
local_file_path = (
    r"C:\Users\marco\Documents\code_classes\GCP-Data-Engineering-Foundations\test_shakesper.txt"
)


def build_storage_client() -> storage.Client:
    """Builds a Storage client using ADC by default, with JSON key fallback."""
    if service_account_json_path:
        return storage.Client.from_service_account_json(service_account_json_path)
    return storage.Client(project=project_id)


storage_client = build_storage_client()


def create_bucket(bucket_name):
    """Creates a new bucket in the specified project."""
    bucket = storage_client.bucket(bucket_name)
    try:
        bucket = storage_client.create_bucket(bucket, location="US")
        print(f"Bucket {bucket.name} created.")
    except Conflict:
        print(
            "Bucket name is not available globally. "
            "Choose another unique name and try again."
        )


def upload_file_to_bucket(
    bucket_name: str,
    file_path: str,
    destination_blob_name: str | None = None,
) -> None:
    """Uploads a local file to a GCS bucket.

    Args:
        bucket_name: Target GCS bucket name.
        file_path: Absolute or relative local file path.
        destination_blob_name: Optional object name in bucket.
    """
    path = Path(file_path)
    if not path.exists() or not path.is_file():
        print(f"Local file not found: {path}")
        return

    bucket = storage_client.bucket(bucket_name)
    if not bucket.exists():
        print(f"Bucket does not exist or is not visible: {bucket_name}")
        return

    blob_name = destination_blob_name or path.name
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(str(path))
    print(f"Uploaded '{path.name}' to 'gs://{bucket_name}/{blob_name}'.")

create_bucket(bucket_name)
upload_file_to_bucket(bucket_name=bucket_name, file_path=local_file_path)