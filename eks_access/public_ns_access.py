import aws_cdk as cdk
from aws_cdk import (
    Stack
)

from aws_cdk.aws_iam import Role, ServicePrincipal, PolicyStatement, PolicyDocument, Effect
from aws_cdk.aws_eks import Cluster, KubernetesManifest

from constructs import Construct


class PublicNsAccessStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Specify the cluster name
        cluster_name = cdk.Fn.import_value(
            'PublicClusterExport')

        # Create an IAM role
        eks_namespace_access_role = Role(
            self, "EksNamespaceAccessRole",
            assumed_by=ServicePrincipal("eks.amazonaws.com")
        )

        # Attach the policy allowing access to the "public" namespace
        eks_namespace_access_role.add_to_policy(
            PolicyStatement(
                actions=[
                    "eks:DescribeCluster",
                ],
                effect=Effect.ALLOW,
                resources=[
                    f"arn:aws:eks:{self.region}:{self.account}:cluster/{cluster_name}"]
            )
        )
