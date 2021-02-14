import os
from collections import namedtuple

import boto3
import pytest
from botocore.stub import Stubber

# prevent boto from looking for IAM creds via metadata while running tests
os.environ["AWS_EC2_METADATA_DISABLED"] = "true"
os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-2"


StubbedClient = namedtuple("StubbedClient", ["stub", "client"])


@pytest.fixture
def fake_kms_client() -> StubbedClient:  # type: ignore
    """Creates a stubbed boto3 CloudFormation client"""
    client = boto3.client("kms")
    with Stubber(client) as stubbed_client:
        yield StubbedClient(stubbed_client, client)
        stubbed_client.assert_no_pending_responses()
