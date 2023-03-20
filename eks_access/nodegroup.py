import aws_cdk as cdk
from aws_cdk import (
    aws_eks as eks,
    aws_ec2 as ec2,
    Stack
)
from constructs import Construct


class NodeGroupStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Retrieve the VPC construct using its Name
        vpc = ec2.Vpc.from_lookup(
            self, 'PrivateEksVpcForNodeGroup', vpc_name='NetworkStack/PrivateEksVpc')
        
        # Import the private_cluster value from the other stack
        private_cluster_name = cdk.Fn.import_value('PrivateClusterExport')

        # Retrieve the private cluster using its name
        private_cluster = eks.Cluster.from_cluster_attributes(
            self, 'PrivateCluster', cluster_name=private_cluster_name, vpc=vpc)

        # Define a node group in a private subnet
        eks.Nodegroup(self, 'PrivateNodegroup',
                      cluster=private_cluster,
                      instance_types=[ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM)],
                      subnets=ec2.SubnetSelection(
                          subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
                      desired_size=1
        )

