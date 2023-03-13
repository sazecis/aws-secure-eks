import aws_cdk as cdk
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
            nat_gateways=0,
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
                ),
                ec2.SubnetConfiguration(
                    cidr_mask=20,
                    name='PublicSubnet2',
                    subnet_type=ec2.SubnetType.PUBLIC
                ),
                ec2.SubnetConfiguration(
                    cidr_mask=20,
                    name='PrivateSubnet2',
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
                )
            ]
        )
 
        # Define the VPC endpoints you need
        endpoints = {
            'STS': ec2.InterfaceVpcEndpointAwsService.STS,
            'EC2': ec2.InterfaceVpcEndpointAwsService.EC2,
            'EC2_MESSAGES': ec2.InterfaceVpcEndpointAwsService.EC2_MESSAGES,
            'EKS': ec2.InterfaceVpcEndpointAwsService.ECR,
            'SSM': ec2.InterfaceVpcEndpointAwsService.SSM,
            'SSM_MESSAGES': ec2.InterfaceVpcEndpointAwsService.SSM_MESSAGES,
            'CLOUDWATCH_LOGS': ec2.InterfaceVpcEndpointAwsService.CLOUDWATCH_LOGS,
        }        
        for name, service in endpoints.items():
            ec2.InterfaceVpcEndpoint(self, f'{name}Endpoint',
                service=service,
                vpc=vpc,
                private_dns_enabled=True
            )