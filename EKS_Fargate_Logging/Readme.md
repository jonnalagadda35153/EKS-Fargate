# EKS Fargate Cluster Logging - Fluentd

> Deamon sets are not allowed in EKS Fargate cluster. Workaround is to use deploy fluentd as sidecar for every application pod

##### Follow the steps below to have fluentd push logs to cloudwatch

1. Create service account fluentd in the required namespace with the command

   **eksctl create iamserviceaccount --name fluentd --namespace <required namespace> --cluster de-iot-sdbx3-fargate --attach-policy-arn arn:aws:iam::aws:policy/AdministratorAccess --override-existing-serviceaccounts --approve**
   
2. Update namespace in fluentd_rbac.yaml file and run the script with the command
   
   **kubectl apply -f fluent_rbac.yaml**
   
3. Now deploy the sample application with fluentd as sidecar with the command 

   **kubectl apply -f sidecar_sample_app.yaml**
   
```
Once the pods are up
 1. Login into the appf container and write sample log with the command
    **kubectl exec -it <pod name> -c appf -n <namespace> bash**
    **echo {"name": "Hello world"} > /opt/cloud/logs/test.log**
    
2. Check if the same file is being read by fluentd container
   **kubectl exec -it <pod name> -c fluentd-sidecar -n <namespace> bash**
   **ls /opt/cloud/logs/** 
   should give the test.log
```
Now you can view logstream **/aws/containerinsights/#{ENV.fetch('CLUSTER_NAME')}/fluentdapp** in the cloudwatch console.

With this demo we are able to run fluentd as sidecar and push logs to cloudwatch

   
