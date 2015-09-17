# DevOps-HW1
##Demo
https://drive.google.com/file/d/0B87f7178bIHnRWF5LTRFTUI1Vm8/view?usp=sharing
## Service Providers
### AWS
AWS is group of web services, cloud computing resources provided by Amazon. One of the services I learned about is the Amazon Elastic Compute Cloud (Amazon EC2). It is designed to make web-scale computing easier for developers and system administrators. It's a kind of cloud hosting, so the users can have full control over the instances they created, this brings a lot of convenience to users. Other advantages like EC2 reduces the time required to obtain and boot new server instances to minutes, allowing users to quickly scale capacity, both up and down, as the computing requirements change. And users can only pay for the capacity they required. Also, AWS has APIs written in different programming languages, everyone can find a suitable one for their developing. 

###Digitalocean
Digital Ocean is also a cloud based hosting provider. It provides virtual servers with full root level ssh access. It provides various distributions of Linux. One can install any package, application on it as required. It is built for developers and it can create a virtual server in less than 1 minute. It also has a developer API, hence all the above tasks can also be done programmatically. 

##Uasge

* Clone this repo
* Run `pip install -r requirement.txt` to install the required packages
* For AWS, create an access key in [AWS console](https://console.aws.amazon.com/iam/home#security_credential), and set the access key according to this [page](https://boto3.readthedocs.org/en/latest/guide/quickstart.html#configuration)
* For Digitalocean, create an access token [here](https://cloud.digitalocean.com/settings/applications). And add this token to environment variables: export DO_TOKEN="token".
* Create a SSH key pair, import the public key to the AWS or Digitalocean. Use the private key to access the instances/droplets.
* Using command `python Provisioning.py -n <number of instances/droplets> -p <provider:aws or DO> -k <private key file>` to create servers and the inventory file.