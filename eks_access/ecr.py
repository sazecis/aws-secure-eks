import aws_cdk as cdk
from aws_cdk import (
    aws_ecr as ecr,
    Stack
)
from constructs import Construct

class EcrStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an Amazon ECR registry
        ecr_repo = ecr.Repository(
            self, "ECRRepo",
            repository_name="demo-ecr-repo"
        )

        # Output the repository URI
        cdk.CfnOutput(
            self, "ECRRepositoryURI",
            value=ecr_repo.repository_uri
        )
