from aws_cdk import (
    aws_ec2 as ec2,
    Stack
)
from constructs import Construct

class NetworkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define a new VPC with two public subnets and two private subnets
        vpc = ec2.Vpc(self, 'PrivateEksVpc',
            ip_addresses=ec2.IpAddresses.cidr('10.0.0.0/16'),
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    cidr_mask=20,
                    name='PublicSubnet',
                    subnet_type=ec2.SubnetType.PUBLIC
                ),
                ec2.SubnetConfiguration(
                    cidr_mask=20,
                    name='PrivateSubnet',
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
                )
            ]
        )
