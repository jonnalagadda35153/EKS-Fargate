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

#Set up OIDC provider with the cluster and create the IAM policy used by the ALB Ingress Controller
oidc_setup = 'eksctl utils associate-iam-oidc-provider --cluster '+str(CLUSTER_NAME)+' --approve'
print(oidc_setup)
os.system(oidc_setup)
print('OIDC setup is done')

#Creating an iamserviceaccount and attaching role.
print('Attaching policy to iamserviceaccount')
attach_policy = 'eksctl create iamserviceaccount --name alb-ingress-controller --namespace kube-system --cluster ' + str(CLUSTER_NAME) +' --attach-policy-arn arn:aws:iam::'+str(AWS_ACCOUNT_ID)+':policy/'+str(ingress_role) +' --override-existing-serviceaccounts --approve '
print(attach_policy)
os.system(attach_policy)
print('Attached Policy')
print("\n")

#Installing  alb-ingress-controller
#Make sure that serviceaccount name created above matches with serviceaccount provided in alb-ingress-controller.yaml file before installing ingress controller
#Please update Cluster Name and VPC id and Region and ServiceAccount in the alb-ingress-controller.yml
apply_ingress = 'kubectl apply -f alb-ingress-controller.yaml'
os.system(apply_ingress)
print('ALB ingress controller is installed')
print('Check logs with the command')
print('kubectl logs -n kube-system $(kubectl get po -n kube-system | egrep -o alb-ingress[a-zA-Z0-9-]+)')
print("\n")