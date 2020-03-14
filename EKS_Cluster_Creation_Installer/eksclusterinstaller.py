# AWS DISCLAMER
# Provided to Customer on 12 March 2020
# ---

# The following files are provided by AWS Professional Services describe the process to create an read-only breakglass role for security within your AWS Automated Landing Zone. These are non-production ready and are to be used for testing purposes.
# These files is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, either express or implied. See the License
# for the specific language governing permissions and limitations under the License.

# (c) 2019 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.
# This AWS Content is provided subject to the terms of the AWS Customer Agreement available at
# http://aws.amazon.com/agreement or other written agreement between Customer and Amazon Web Services, Inc.​


#!/usr/bin/env python3
import boto3
import subprocess
import os
import time
import json
import re
import time
import sys
import configparser
import sys
import configparser
import yaml

stream = open('eksClusterCreation.yml', 'r')
data = yaml.load(stream)
eks_cluster = data.get("metadata").get("name")
print('\n')
print('\n')
print('EKS Cluster Name: '+eks_cluster)


length = len(sys.argv)
vpcparam = ''
if length > 1:
    vpcparam = sys.argv[1]

eks_curl = 'curl --location "https://github.com/weaveworks/eksctl/releases/download/latest_release/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp'
kubectl_curl = 'curl -o kubectl https://amazon-eks.s3-us-west-2.amazonaws.com/1.14.6/2019-08-22/bin/linux/amd64/kubectl'
kubectl_chmod = 'chmod +x ./kubectl'
kubectl_binary = 'mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$HOME/bin:$PATH'
kubectl_home = "echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc"
kubectl_version = 'kubectl version --short --client'
eks_curl_move = 'sudo mv -v /tmp/eksctl /usr/local/bin'

if vpcparam == 'newvpc':
    eks_create_cluster = 'eksctl create cluster'
    print("\033[1;32;40m Creating EKS Cluster in a new VPC  \n")
else:
    eks_create_cluster = 'eksctl create cluster -f eksClusterCreation.yml'
    print("\033[1;32;40m Creating EKS Cluster in an existing VPC  \n")
    
eks_version = 'eksctl version'
#eks_nodes = 'kubectl get nodes -o wide'
IAM_auth_download = "curl -o aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/1.15.10/2020-02-22/bin/linux/amd64/aws-iam-authenticator"
IAM_auth_install = "chmod +x ./aws-iam-authenticator"
IAM_binary_copy = "mkdir -p $HOME/bin && cp ./aws-iam-authenticator $HOME/bin/aws-iam-authenticator && export PATH=$HOME/bin:$PATH"
IAM_path_var = "echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc"
jq_install = 'sudo yum -y install jq gettext'
check = "for command in kubectl aws-iam-authenticator jq envsubst;   do     which $command &>/dev/null && echo '$command in path' || echo '$command NOT FOUND';   done"

#Update helm to versions3
helm_download = 'curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 > get_helm.sh'
helm_modify = 'chmod +x get_helm.sh'
helm_install = './get_helm.sh'
rbac_install = 'kubectl apply -f RBAC.yaml'
helm_stabe_repo = 'helm repo add stable https://kubernetes-charts.storage.googleapis.com/'
#metrics_namespace = 'kubectl create namespace metrics'
metricserver_install = 'helm install metrics-server stable/metrics-server --version 2.9.0 --namespace kube-system'
hpa_test = 'kubectl get hpa --all-namespaces'


print('\033[1m' + "Downloading eksctl")
os.system(eks_curl)
print('\n')
print('\033[1m' + "Installing eksctl")
os.system(eks_curl_move)
print('\n')
print('\033[1m' + "eksctl version")
os.system(eks_version)
print('\n')
print('\033[1m' + "Downloading and Installing Kubectl 1.14")
print("Download kubectl")
os.system(kubectl_curl)
print("Modifying Binary access")
os.system(kubectl_chmod)
os.system(kubectl_binary)
os.system(kubectl_home)
print('\033[1m'+"Kubectl version")
os.system(kubectl_version)
print('\n')
print('\033[1m' + "Creating EKS Cluster")
os.system(eks_create_cluster)
print('\n')
print('\033[1m' + "Download IAM Authenticator")
os.system(IAM_auth_download)
print('\033[1m' + "Install IAM Authenticator")
os.system(IAM_auth_install)
print('\033[1m' + "Edit Binary access")
os.system(IAM_binary_copy)
print('\033[1m' + "Copy Binary to path")
os.system(IAM_path_var)
print('\n')
print('\033[1m' + "Install JQ")
os.system(jq_install)
print('\n')
print('\033[1m' + "Checking the installed Libraries")
os.system(check)
print('\n')
print('\033[1m' + "Downloading helm")
os.system(helm_download)
print('\n')
print('\033[1m' + "Modifying helm")
os.system(helm_modify)
print('\n')
print('\033[1m' + "Installing helm")
os.system(helm_install)
print('\n')
print('\033[1m' + "Installing stable helm charts")
os.system("helm repo add stable https://kubernetes-charts.storage.googleapis.com/")
print('\n')
print("Metrics Server Installation")
os.system(metricserver_install)
print('\n')
time.sleep(180)
print('\033[1m' + "HPA Test")
os.system(hpa_test)
print('\n')
print("Updating EKS Cluster Cotrol Plane Security group")
eks_sg_id_cli = 'aws eks describe-cluster --region us-east-1 --name '+str(eks_cluster)+' --query '+"""'cluster.resourcesVpcConfig.securityGroupIds'""" + ' --output text'
print(eks_sg_id_cli)
eks_sg_id = os.popen(eks_sg_id_cli).read().split('\n')[0]
print(eks_sg_id)
eks_sg_update_cli = 'aws ec2 authorize-security-group-ingress --group-id '+str(eks_sg_id)+' --ip-permissions IpProtocol=tcp,FromPort=443,ToPort=443,IpRanges='+"""'[{CidrIp=0.0.0.0/0}]'"""
print(eks_sg_update_cli)
os.system(eks_sg_update_cli)
print("Enabling Private Access for the Cluster")
eks_private_access = 'aws eks update-cluster-config --region us-east-1 --name '+str(eks_cluster)+' --resources-vpc-config endpointPublicAccess=true,endpointPrivateAccess=true'
os.system(eks_private_access)
print('\n')
print("End Cluster Creation")