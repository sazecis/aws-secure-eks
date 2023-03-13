import aws_cdk as cdk
from aws_cdk import (
    aws_eks as eks,
    aws_ec2 as ec2,
    Stack
)
from constructs import Construct

class PrivateStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Retrieve the VPC construct using its Name
        vpc = ec2.Vpc.from_lookup(self, 'PrivateEksVpc', vpc_name='PrivateEksVpc')

        # Define EKS Cluster with private access
        private_cluster = eks.Cluster(self, 'PrivateCluster',
            version=eks.KubernetesVersion.V1_23,
            default_capacity=1,
            endpoint_access=eks.EndpointAccess.PRIVATE,
            vpc=vpc
        )