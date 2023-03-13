import aws_cdk as core
import aws_cdk.assertions as assertions

from eks_access.private import PrivateStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_private_eks_access/aws_private_eks_access_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PrivateStack(app, "private")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
