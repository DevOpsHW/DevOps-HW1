import boto.ec2
import os
from boto.ec2 import address

conn = boto.ec2.connect_to_region('us-east-1')

# conn.run_instances(
#         'ami-d05e75b8',
#         key_name='mac',
#         instance_type='t2.micro',
#         security_groups=['default'],
#         min_count=3,
#         max_count=4,
#         # instance_profile_name = 'test1'
#     )

status = conn.get_all_instance_status()[0]
conn.get_all_instances()[2].instances

conn.get_all_reserved_instances()

ip = conn.get_only_instances()[0].ip_address

print conn.get_all_instance_status()[0].state_name


def createInventory(key_file):
    id = conn.get_only_instances()[0].id
    ip = conn.get_only_instances()[0].ip_address
    key_file_path = os.path.abspath(key_file)
    user = 'ubuntu'
    s = '%s ansible_ssh_host=%s ansible_ssh_user=%s ansible_ssh_private_key_file=%s' % (id, ip, user, key_file_path,)
    f = open('inventory', 'ab')
    print >> f, s
    # f.save()
    f.close()

# createInventory('private.key')