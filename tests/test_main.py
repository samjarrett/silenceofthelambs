# pylint:disable=redefined-outer-name
import base64
import os

from silenceofthelambs import main

from . import stubs
from .conftest import StubbedClient


def test_get_values_to_decrypt():
    """Tests main.get_values_to_decrypt()"""
    fake_environ = {"MY": "thing", "SOMETHING": "else"}
    assert dict() == main.get_values_to_decrypt(fake_environ)

    fake_environ = {
        "MY": "thing",
        "SOMETHING": "else",
        "KMS_ENCRYPTED_SOMETHING_ELSE": "sure",
    }
    assert {"SOMETHING_ELSE": "sure"} == main.get_values_to_decrypt(fake_environ)


def test_decrypt_value(fake_kms_client: StubbedClient):
    """Tests main.decrypt_value()"""
    value = "hello"
    encoded_value = base64.b64encode(value.encode()).decode()

    stubs.stub_decrypt(fake_kms_client.stub, value.encode(), value)
    assert value == main.decrypt_value(fake_kms_client.client, encoded_value)

    # test an invalid value
    stubs.stub_decrypt_error(fake_kms_client.stub, value.encode())
    assert not main.decrypt_value(fake_kms_client.client, encoded_value)


def test_decrypt(fake_kms_client: StubbedClient):
    """Tests main.decrypt()"""
    value = "hello"
    encoded_value = base64.b64encode(value.encode()).decode()
    os.environ.update(
        {
            "MY": "thing",
            "SOMETHING": "",
            "KMS_ENCRYPTED_SOMETHING": encoded_value,
        }
    )

    stubs.stub_decrypt(fake_kms_client.stub, value.encode(), "my_decoded_value")
    main.decrypt(kms_client=fake_kms_client.client)

    assert "SOMETHING" in os.environ
    assert os.environ.get("SOMETHING") == "my_decoded_value"

    first_value = "hello"
    encoded_first_value = base64.b64encode(first_value.encode()).decode()
    second_value = "my_value"
    encoded_second_value = base64.b64encode(second_value.encode()).decode()
    variables = {
        "MY": "thing",
        "SOMETHING": "",
        "SOMETHING_ELSE": "",
        "KMS_ENCRYPTED_SOMETHING": encoded_first_value,
        "KMS_ENCRYPTED_SOMETHING_ELSE": encoded_second_value,
    }

    stubs.stub_decrypt(fake_kms_client.stub, first_value.encode(), "my_decoded_value")
    stubs.stub_decrypt(
        fake_kms_client.stub, second_value.encode(), "another_decoded_value"
    )
    main.decrypt(kms_client=fake_kms_client.client, variables=variables)

    assert "SOMETHING" in os.environ
    assert os.environ.get("SOMETHING") == "my_decoded_value"
    assert "SOMETHING_ELSE" in os.environ
    assert os.environ.get("SOMETHING_ELSE") == "another_decoded_value"
