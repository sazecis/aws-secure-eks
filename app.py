#!/usr/bin/env python3
import boto3

import aws_cdk as cdk

from eks_access.private_eks import PrivateEksStack
from eks_access.public_eks import PublicEksStack
from eks_access.network import NetworkStack
from eks_access.bastion import BastionStack
from eks_access.nodegroup import NodeGroupStack

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
PrivateEksStack(app, "PrivateEksStack", env=env)
PublicEksStack(app, "PublicEksStack", env=env)
BastionStack(app, "BastionStack", env=env)
NetworkStack(app, "NetworkStack", env=env)
NodeGroupStack(app, "NodeGroupStack", env=env)

app.synth()
