import boto3
import configparser
import sys
import os
import time

config = configparser.ConfigParser()
config.read('ingress_param.ini')

#workernode_role_names = str(config['alb']['workernodes_instance_role_name'])
#workernode_role = workernode_role_names.split(",")
CLUSTER_NAME = str(config['alb']['CLUSTER_NAME'])
print('Cluster is: '+CLUSTER_NAME)

AWS_ACCOUNT_ID = str(config['alb']['AWS_ACCOUNT_ID'])
print('Account id: '+AWS_ACCOUNT_ID)

#Attaching IAM policy for ALB ingress controller
'''
for i in range(0,len(workernode_role)):
    attach_policy = 'aws iam put-role-policy --role-name '+ str(workernode_role[i]) +' --policy-name ALB_Ingress_policy --policy-document file://alb_ingress_IAM_policy.json'
    os.system(attach_policy)
    print('Attached Policy to the worker nodes with role name '+str(workernode_role[i]))
    time.sleep(3)
'''

'''
create_policy = 'aws iam create-policy --policy-name ALB_Ingress_policy --policy-document file://alb_ingress_IAM_policy.json'
os.system(create_policy)
print('Created ALB_Ingress_policy')
print("\n")
'''

#Applying RBAC in the Kube-system namespace to enable ALB Creation and Communication
apply_rbac = 'kubectl apply -f RBAC.yaml'
print("Applying RBAC")
os.system(apply_rbac)

#Attaching policy to iamserviceaccount
print('Attaching policy to iamserviceaccount')
attach_policy = 'eksctl create iamserviceaccount --name alb-ingress-controller --namespace kube-system --cluster ' + str(CLUSTER_NAME) +' --attach-policy-arn arn:aws:iam::057929149431:policy/alb-ingress-role --override-existing-serviceaccounts --approve '
print(attach_policy)
os.system(attach_policy)
print('Attached Policy')
print("\n")

#Installing  alb-ingress-controller
#Please update Cluster Name and VPC id and Region and ServiceAccount in the alb-ingress-controller.yml
apply_ingress = 'kubectl apply -f alb-ingress-controller.yaml'
os.system(apply_ingress)
print("\n")