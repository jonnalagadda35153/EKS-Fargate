### Python Script Deploys RBAC Roles and RoleBindings needed by the AWS ALB Ingress controller

Collect instance profile names and update the ini file workernodes_instance_role_name with the profile names as comma separated values

### Edit the AWS ALB Ingress controller YAML to include the clusterName of the Kubernetes (or) Amazon EKS cluster. Edit the –cluster-name flag and replace it with the name of Amazon EKS cluster. 

You can check the Name of the Cluster with the CLI aws eks list-clusters

Verify that the deployment was successful and the controller started:

kubectl logs -n kube-system $(kubectl get po -n kube-system | egrep -o alb-ingress[a-zA-Z0-9-]+)
You should be able to see the following output:

-------------------------------------------------------------------------------
AWS ALB Ingress controller
  Release:    v1.0.0
  Build:      git-c25bc6c5
  Repository: https://github.com/kubernetes-sigs/aws-alb-ingress-controller
-------------------------------------------------------------------------------
