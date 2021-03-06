# EKS Fargate Cluster Logging - Fluentd

> Deamon sets are not allowed in EKS Fargate cluster. Workaround is to use deploy fluentd as sidecar for every application pod

##### Follow the steps below to have fluentd push logs to cloudwatch

1. Create service account fluentd in the required namespace with the command

   **eksctl create iamserviceaccount --name spring-sa --namespace {namespace}  --cluster {clsutername} --attach-policy-arn arn:aws:iam::aws:policy/AdministratorAccess --override-existing-serviceaccounts --approve**
   
2. Update namespace,serviceAccount in fluentd_rbac.yaml file and run the script with the command
   
   **kubectl apply -f fluent_rbac.yaml**
   
3. Now deploy the sample application with fluentd as sidecar with the command 

   **kubectl apply -f sidecar_sample_app.yaml**
   
> Update region, clustername, serviceAccount in the sidecar_sample_app.yaml file


Now you can view logstream **/aws/containerinsights/{clustername}/springapp** in the cloudwatch console.

With this demo we are able to run fluentd as sidecar and push logs to cloudwatch

Quip: https://quip-amazon.com/HaapAaBOaGVo/Application-Logging-with-EKS-on-Fargate-using-Fluentd-CloudWatch

   
