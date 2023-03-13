#!/usr/bin/env python3
import boto3

import aws_cdk as cdk

from eks_access.private import PrivateStack
from eks_access.public import PublicStack
from eks_access.network import NetworkStack
from eks_access.bastion import BastionStack

# Create a new session using the current AWS profile
session = boto3.session.Session()

# Get the current region
region = session.region_name

# Get the current account ID
sts_client = session.client('sts')
account_id = sts_client.get_caller_identity().get('Account')

env = cdk.Environment(
    account=account_id,
    region=region
)

app = cdk.App()
PrivateStack(app, "PrivateStack", env=env)
PublicStack(app, "PublicStack", env=env)
BastionStack(app, "BastionStack", env=env)
NetworkStack(app, "NetworkStack", env=env)

app.synth()
