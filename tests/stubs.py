KMS_KEY_ID = (
    "arn:aws:kms:ap-southeast-2:123456789012:key/aaaaaaaa-1111-aaaa-aaaa-aaaaaaaaaaaa"
)


def stub_decrypt(
    stubber,
    ciphertext_encoded: bytes,
    decrypted_value: str,
):
    """Stubs KMS decrypt responses"""
    response = {
        "KeyId": KMS_KEY_ID,
        "Plaintext": decrypted_value.encode(),
        "EncryptionAlgorithm": "SYMMETRIC_DEFAULT",
    }

    stubber.add_response(
        "decrypt",
        response,
        expected_params={"CiphertextBlob": ciphertext_encoded},
    )


def stub_decrypt_error(
    stubber,
    ciphertext_encoded: bytes,
    exception_type: str = "InvalidCiphertextException",
):
    """Stubs KMS decrypt responses where there is an error"""
    stubber.add_client_error(
        "decrypt",
        exception_type,
        exception_type,
        400,
        expected_params={"CiphertextBlob": ciphertext_encoded},
    )
