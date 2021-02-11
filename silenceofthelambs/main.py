import os
import base64
from typing import Dict, Optional

import boto3


def get_values_to_decrypt() -> Dict[str, str]:
    """Filters the environ pseudo-dict and identifies key/vals for decryption"""
    return {
        key[14:]: value
        for key, value in os.environ.items()
        if key.startswith("KMS_ENCRYPTED_")
    }


def __decrypt(kms_client: boto3.client, value: str) -> Optional[str]:
    """Decrypt a single value"""
    try:
        result = kms_client.decrypt(CiphertextBlob=base64.b64decode(value))
        return result["Plaintext"].decode()
    except kms_client.exceptions.ClientError:
        return None


def decrypt(kms_client: Optional[boto3.client] = None):
    """Decrypts encrypted keys in the environment"""
    if not kms_client:
        kms_client = boto3.client("kms")

    values = get_values_to_decrypt()
    for key, value in values.items():
        decrypted_value = __decrypt(kms_client, value)
        if decrypted_value:
            os.environ[key] = decrypted_value
