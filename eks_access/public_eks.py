import aws_cdk as cdk
from aws_cdk import (
    aws_eks as eks,
    aws_ec2 as ec2,
    Stack
)
from constructs import Construct

class PublicEksStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define EKS Cluster with public access
        public_cluster = eks.Cluster(self, 'PublicCluster',
            version=eks.KubernetesVersion.V1_23,
            default_capacity=1,
            default_capacity_instance=ec2.InstanceType.of(
                ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM),
            endpoint_access=eks.EndpointAccess.PUBLIC
        )

        # Export the private_cluster value
        cdk.CfnOutput(self, 'PublicClusterOutput',
                      value=public_cluster.cluster_name,
                      export_name='PublicClusterExport'
                      )
