from google.cloud import storgage
import os
from dotenv import load_dotenv

load_dotenv()

service_account_key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
bucket_name = os.environ["GCS_BUCKET_NAME"]

storage_client = storgage.Client.from_service_account_json(service_account_key_path)
bucket = storage_client.bucket(bucket_name)

def create_bucket(bucket_name):
    """Creates a new bucket."""
    bucket = storage_client.bucket(bucket_name)
    bucket.location = "US"
    bucket = storage_client.create_bucket(bucket)
    print(f"Bucket {bucket.name} created.")
    
create_bucket(bucket_name)