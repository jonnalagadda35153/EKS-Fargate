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

import boto3
import configparser
import sys
import os
import time

config = configparser.ConfigParser()
config.read('ingress_param.ini')

CLUSTER_NAME = str(config['alb']['CLUSTER_NAME'])
print('Cluster is: '+CLUSTER_NAME)

AWS_ACCOUNT_ID = str(config['alb']['AWS_ACCOUNT_ID'])
print('Account id: '+AWS_ACCOUNT_ID)

ingress_role = str(config['alb']['ingress_role'])
print("Ingress IAM role: "+ingress_role)

#Applying RBAC in the Kube-system namespace to enable ALB Creation and Communication
apply_rbac = 'kubectl apply -f RBAC.yaml'
print("Applying RBAC")
os.system(apply_rbac)

#Creating an iamserviceaccount and attaching role.
print('Attaching policy to iamserviceaccount')
attach_policy = 'eksctl create iamserviceaccount --name alb-ingress-controller --namespace kube-system --cluster ' + str(CLUSTER_NAME) +' --attach-policy-arn arn:aws:iam::'+str(AWS_ACCOUNT_ID)+':policy/'+str(ingress_role) +'--override-existing-serviceaccounts --approve '
print(attach_policy)
os.system(attach_policy)
print('Attached Policy')
print("\n")



#Installing  alb-ingress-controller
#Make sure that serviceaccount name created above matches with serviceaccount provided in alb-ingress-controller.yaml file before installing ingress controller
#Please update Cluster Name and VPC id and Region and ServiceAccount in the alb-ingress-controller.yml
apply_ingress = 'kubectl apply -f alb-ingress-controller.yaml'
os.system(apply_ingress)
print("\n")