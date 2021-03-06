import os
import time
import boto3

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

def createInstances(num, key='mac', security_group='default'):
    instances = ec2.create_instances(
        ImageId='ami-d05e75b8',
        MinCount=num,
        MaxCount=num,
        SecurityGroups=[security_group],
        InstanceType='t2.micro',
        KeyName=key
    )
    ids = [ins.id for ins in instances]
    print "Instances created, IDs: ", ids
    ips = []
    for id in ids:
        ips.append(ec2.Instance(id).public_ip_address)
    while(True):
        if all(ips):
            print "Get IPs: ", ips
            break
        else:
            print "Waiting for IP address"
            time.sleep(5)
            ips = []
            for id in ids:
                ips.append(ec2.Instance(id).public_ip_address)
    return instances

def createKeyPairs(name, public_key_file):
    f = open(public_key_file, 'r')
    key = f.read()
    f.close()
    key_pair = ec2.import_key_pair(
        KeyName=name,
        PublicKayMaterial=key
    )
    return key_pair

def createSecurityGroup(name, description):
    sg = ec2.create_security_group(
        GroupName=name,
        Description=description
    )
    sg.authorize_ingress(
        IpProtocol='-1',
        CidrIp='0.0.0.0/0'
    )


def createInventory(instances, key_file):
    key_file_path = os.path.abspath(key_file)
    user = 'ubuntu'
    ids = [ins.id for ins in instances]
    ips = []
    for id in ids:
        ips.append(ec2.Instance(id).public_ip_address)
    f = open('inventory', 'ab')
    print "Writing to inventory"
    for i in range(len(ips)):
        s = '%s ansible_ssh_host=%s ansible_ssh_user=%s ansible_ssh_private_key_file=%s' % (ids[i], ips[i], user, key_file_path,)
        print s
        print >> f, s
    f.close()

def checkIfAllActive(instances):
    ids = [ins.id for ins in instances]
    status = client.describe_instance_status(InstanceIds=ids)['InstanceStatuses']
    # if all([s['InstanceStatus']['Details'][0]['Status'] == 'passed' and s['SystemStatus']['Details'][0]['Status'] == 'passed' for s in status]):
    if all([s['InstanceState']['Name'] == 'running' for s in status]):
        return True
    else:
        return False
