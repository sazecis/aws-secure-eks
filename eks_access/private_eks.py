import aws_cdk as cdk
from aws_cdk import (
    aws_eks as eks,
    aws_ec2 as ec2,
    aws_iam as iam,
    Stack
)
from constructs import Construct
from aws_cdk.lambda_layer_kubectl_v24 import KubectlV24Layer

class PrivateEksStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Retrieve the VPC construct using its Name
        vpc = ec2.Vpc.from_lookup(
            self, 'PrivateEksVpc', vpc_name='NetworkStack/PrivateEksVpc')

        # Define EKS Cluster with private access
        private_cluster = eks.Cluster(self, 'PrivateCluster',
                                      version=eks.KubernetesVersion.V1_24,
                                      default_capacity=0,
                                      endpoint_access=eks.EndpointAccess.PRIVATE,
                                      vpc=vpc,
                                      kubectl_layer=KubectlV24Layer(self, 'KubectlV24Layer')
                                      )

        # Define a custom managed policy that allows the eks:DescribeCluster action on the EKS cluster
        custom_policy = iam.ManagedPolicy(self, 'BastionEksPolicy',
                                          managed_policy_name='BastionEksPolicy',
                                          statements=[
                                              iam.PolicyStatement(
                                                  effect=iam.Effect.ALLOW,
                                                  actions=[
                                                      'eks:DescribeCluster'],
                                                  resources=[
                                                      private_cluster.cluster_arn]
                                              )
                                          ]
                                          )
        bastion_role = iam.Role.from_role_name(
            self, 'BastionRole', role_name='BastionRole')

        # Attach the custom managed policy to the IAM role
        bastion_role.add_managed_policy(custom_policy)

        private_cluster.aws_auth.add_masters_role(role=bastion_role)

        # Export the private_cluster value
        cdk.CfnOutput(self, 'PrivateClusterOutput',
                       value=private_cluster.cluster_name,
                       export_name='PrivateClusterExport'
                       )

        # Export the additional security group of the EKS cluster
        cdk.CfnOutput(self, 'AdditionalSecurityGroupOutput',
                       value=private_cluster.kubectl_security_group.security_group_id,
                       export_name='AdditionalSecurityGroupExport'
                       )
