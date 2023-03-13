import aws_cdk as cdk
from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_ssm as ssm,
    Stack
)
from constructs import Construct

class BastionStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Retrieve the VPC construct using its Name
        vpc = ec2.Vpc.from_lookup(self, 'PrivateEksVpc', vpc_name='PrivateEksVpc')

        # Create a new security group with no inbound rules
        security_group = ec2.SecurityGroup(self, 'BastionSecurityGroup',
            vpc=vpc,
            allow_all_outbound=True,
            security_group_name='bastion-security-group'
        )

        # Create a new SSM parameter to store the kubectl version
        kubectl_version_param = ssm.StringParameter(self, 'KubectlVersion',
            parameter_name='/bastion/kubectl/version',
            string_value='1.23.0'
        )

        # Create a new EC2 instance with the custom security group and instance profile
        ec2.Instance(self, 'BastionInstance',
            instance_type=ec2.InstanceType('t3.micro'),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=vpc,
            security_group=security_group,
            role=iam.Role.from_role_arn(self, 'BastionRole', role_arn='arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore'),
            block_devices=[
                ec2.BlockDevice(
                    device_name='/dev/xvda',
                    volume=ec2.BlockDeviceVolume.ebs(
                        volume_size=10,
                        delete_on_termination=True
                    )
                )
            ]
        ).add_user_data('UserData', f"""#!/bin/bash
# Install kubectl
yum install -y curl
curl -LO https://storage.googleapis.com/kubernetes-release/release/v{kubectl_version_param.string_value}/bin/linux/amd64/kubectl
chmod +x ./kubectl
mv ./kubectl /usr/local/bin/kubectl
""")