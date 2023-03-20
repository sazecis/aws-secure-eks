from aws_cdk import (
    aws_iam as iam,
    Stack
)
from constructs import Construct

class IamStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a new IAM role
        bastion_role = iam.Role(self, 'BastionRole',
                                assumed_by=iam.ServicePrincipal(
                                    'ec2.amazonaws.com'),
                                role_name='BastionRole'
                                )

        # Attach the AmazonSSMManagedInstanceCore managed policy to the IAM role
        bastion_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSSMManagedInstanceCore'))
