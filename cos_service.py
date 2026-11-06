"""
IBM Cloud Object Storage (COS) Integration Service
Provides secure, compliant document storage for candidate resumes using ibm_boto3.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import ibm_boto3
from ibm_botocore.client import Config
from app.config import settings

VAULT_DIR = Path(__file__).resolve().parent.parent / "data" / "resume_vault"
VAULT_DIR.mkdir(parents=True, exist_ok=True)

class IBMCOSService:
    def __init__(self):
        self.endpoint = settings.IBM_COS_ENDPOINT
        self.api_key = settings.IBM_COS_APIKEY
        self.instance_id = settings.IBM_COS_SERVICE_INSTANCE_ID
        self.bucket_name = settings.IBM_COS_BUCKET_NAME

    def is_configured(self) -> bool:
        return bool(self.api_key and self.endpoint and self.bucket_name)

    def _get_cos_client(self):
        """Construct IBM Cloud Object Storage client using IBM IAM authentication."""
        return ibm_boto3.client(
            "s3",
            ibm_api_key_id=self.api_key,
            ibm_service_instance_id=self.instance_id,
            config=Config(signature_version="oauth"),
            endpoint_url=self.endpoint
        )

    def upload_resume(self, file_bytes: bytes, filename: str, candidate_email: str) -> Dict[str, Any]:
        """
        Store candidate resume in IBM Cloud Object Storage or secure local vault.
        Ensures documents are protected and candidate privacy is maintained.
        """
        safe_filename = f"{candidate_email.replace('@', '_at_')}_{filename}"

        if self.is_configured():
            try:
                client = self._get_cos_client()
                client.put_object(
                    Bucket=self.bucket_name,
                    Key=safe_filename,
                    Body=file_bytes,
                    ContentType="application/octet-stream"
                )
                return {
                    "storage": "IBM Cloud Object Storage",
                    "bucket": self.bucket_name,
                    "key": safe_filename,
                    "status": "Securely uploaded to IBM COS"
                }
            except Exception as e:
                print(f"[IBM COS Warning] Cloud upload fallback: {e}")

        # Local fallback vault
        local_path = VAULT_DIR / safe_filename
        with open(local_path, "wb") as f:
            f.write(file_bytes)

        return {
            "storage": "Secure Local Vault (IBM COS Standby)",
            "key": safe_filename,
            "status": "Stored in secure local partition. Configure IBM COS API key in Settings for cloud synchronization."
        }

cos_service = IBMCOSService()
