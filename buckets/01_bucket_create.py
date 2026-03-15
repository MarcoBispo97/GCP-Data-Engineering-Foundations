from dataclasses import dataclass
import logging
import os
from typing import Optional

from google.api_core.exceptions import Conflict
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

def setup_logging(level: int = logging.INFO) -> None:
    """Configures the root logging format and level.

    Args:
        level: Global logging level.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    )


@dataclass(frozen=True)
class AppConfig:
    """Represents environment configuration for GCS bucket operations.

    Attributes:
        project_id: Google Cloud project ID.
        bucket_name: Target GCS bucket name.
        location: Target bucket location.
        service_account_key_path: Optional service account JSON path.
    """

    project_id: str
    bucket_name: str
    location: str = "US"
    service_account_key_path: Optional[str] = None

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Builds configuration from environment variables.

        Returns:
            A validated AppConfig instance.

        Raises:
            ValueError: If required environment variables are missing.
        """
        config_logger = logging.getLogger("app.config")

        project_id = os.getenv("GCP_PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT")
        bucket_name = os.getenv("GCS_BUCKET_NAME")
        service_account_key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        location = os.getenv("GCS_BUCKET_LOCATION", "US")

        if not project_id:
            raise ValueError(
                "Set GCP_PROJECT_ID (or GOOGLE_CLOUD_PROJECT) in environment variables."
            )
        if not bucket_name:
            raise ValueError("Set GCS_BUCKET_NAME in environment variables.")

        config_logger.info("Environment configuration loaded successfully.")
        config_logger.debug(
            "Config values project_id=%s bucket_name=%s location=%s using_key=%s",
            project_id,
            bucket_name,
            location,
            bool(service_account_key_path),
        )

        return cls(
            project_id=project_id,
            bucket_name=bucket_name,
            location=location,
            service_account_key_path=service_account_key_path,
        )


class StorageClientFactory:
    """Creates configured `google.cloud.storage.Client` instances."""

    def __init__(self, config: AppConfig) -> None:
        """Initializes the factory.

        Args:
            config: Application configuration.
        """
        self.config = config
        self.logger = logging.getLogger("app.auth")

    def build(self) -> storage.Client:
        """Builds the storage client using ADC or service account JSON.

        Returns:
            A configured Storage client.
        """
        os.environ.setdefault("GOOGLE_CLOUD_PROJECT", self.config.project_id)

        if self.config.service_account_key_path:
            self.logger.info("Creating storage client using service account JSON.")
            return storage.Client.from_service_account_json(
                self.config.service_account_key_path,
                project=self.config.project_id,
            )

        self.logger.info("Creating storage client using Application Default Credentials (ADC).")
        return storage.Client(project=self.config.project_id)


class BucketService:
    """Provides GCS bucket operations."""

    def __init__(self, client: storage.Client, config: AppConfig) -> None:
        """Initializes the service.

        Args:
            client: Google Cloud Storage client.
            config: Application configuration.
        """
        self.client = client
        self.config = config
        self.logger = logging.getLogger("app.bucket")
        self.connection_logger = logging.getLogger("app.connection")

    def test_connection(self) -> None:
        """Tests GCS connection by requesting project buckets metadata.

        Raises:
            Exception: If the API call fails for auth/network/permission reasons.
        """
        self.connection_logger.info(
            "Testing GCS connection for project '%s'.",
            self.config.project_id,
        )
        self.client.list_buckets(project=self.config.project_id, max_results=1)
        self.connection_logger.info("GCS connection test succeeded.")

    def bucket_exists(self) -> bool:
        """Checks whether the configured bucket already exists.

        Returns:
            True if bucket exists, otherwise False.
        """
        self.logger.info("Checking if bucket '%s' already exists.", self.config.bucket_name)
        existing_bucket = self.client.lookup_bucket(self.config.bucket_name)
        exists = existing_bucket is not None
        if exists:
            self.logger.warning("Bucket '%s' already exists.", self.config.bucket_name)
        else:
            self.logger.info("Bucket '%s' does not exist yet.", self.config.bucket_name)
        return exists

    def create_bucket_if_missing(self) -> None:
        """Creates the configured bucket if it does not already exist.

        This method is idempotent: it logs and exits when the bucket already exists.
        """
        self.test_connection()

        if self.bucket_exists():
            self.logger.warning("No action taken because the bucket name is already in use.")
            return

        bucket = self.client.bucket(self.config.bucket_name)
        self.logger.info(
            "Creating bucket '%s' in location '%s'.",
            self.config.bucket_name,
            self.config.location,
        )

        try:
            created_bucket = self.client.create_bucket(bucket, location=self.config.location)
            self.logger.info("Bucket '%s' created successfully.", created_bucket.name)
        except Conflict:
            self.logger.warning(
                "Bucket '%s' already exists. No action taken.",
                self.config.bucket_name,
            )


def main() -> None:
    """Runs the bucket creation flow."""
    setup_logging()
    app_logger = logging.getLogger("app.main")

    config = AppConfig.from_env()
    client = StorageClientFactory(config).build()
    service = BucketService(client, config)

    app_logger.info("Starting bucket operation flow.")
    service.create_bucket_if_missing()
    app_logger.info("Bucket operation flow finished.")


if __name__ == "__main__":
    main()


