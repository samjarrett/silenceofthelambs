import base64
import os
from typing import Dict, Optional

import boto3


def get_values_to_decrypt(variables: Dict[str, str]) -> Dict[str, str]:
    """Filters the environ pseudo-dict and identifies key/vals for decryption"""
    return {
        key[14:]: value
        for key, value in variables.items()
        if key.startswith("KMS_ENCRYPTED_")
    }


def decrypt_value(kms_client: boto3.client, value: str) -> Optional[str]:
    """Decrypt a single value"""
    try:
        decoded = base64.b64decode(value)
        result = kms_client.decrypt(CiphertextBlob=decoded)
        return result["Plaintext"].decode()
    except kms_client.exceptions.ClientError:
        return None


def decrypt(
    kms_client: Optional[boto3.client] = None,
    variables: Optional[Dict[str, str]] = None,
):
    """Decrypts encrypted keys in the environment"""
    if not kms_client:  # pragma: no cover
        kms_client = boto3.client("kms")

    if not variables:
        variables = os.environ  # type: ignore

    values = get_values_to_decrypt(variables)  # type: ignore
    for key, value in values.items():
        decrypted_value = decrypt_value(kms_client, value)
        if decrypted_value:
            os.environ[key] = decrypted_value
