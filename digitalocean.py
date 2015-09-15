import requests
import json
import os
import time
import sys



class Droplet():
    def __init__(self, *args, **kwargs):
        if kwargs:
            self.id = kwargs['id']
            self.name = kwargs['name']
            self.ip = kwargs['networks']['v4'][0]['ip_address']
            self.status = kwargs['status']
        else:
            self.id = args[0]
            self.name = args[1]
            self.ip = None
            self.status = None

    def updateStatus(self, conn):
        r = conn.retrieveDroplet(self.id)
        self.status = r['droplet']['status']
        if self.status == 'active':
            self.ip = r['droplet']['networks']['v4'][0]['ip_address']

    def checkStatus(self, conn):
        self.status = conn.retrieveDroplet(self.id)['droplet']['status']
        print "Droplet status is " + self.status
        return self.status

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return "ID: %d, Name: %s, IP: %s, Status: %s" %(self.id, self.name, self.ip, self.status)



class Digitalocean():
    def __init__(self, token):
        self.headers = {
            'Authorization': 'Bearer ' + token,
            "Content-Type": 'application/json'
        }
        self.droplets = []
        self.ips = []

    def listRegions(self):
        r = requests.get("https://api.digitalocean.com/v2/regions", headers=self.headers)
        for region in r.json()['regions']:
            print region['slug']

    def listImages(self):
        r = requests.get("https://api.digitalocean.com/v2/images", headers=self.headers)
        for image in r.json()['images']:
            print image['slug']

    def createDroplet(self, name, region, imageName):
        data = {
            "name": name,
            "region": region,
            "size": "512mb",
            "ssh_keys": self.getSSHkeyID(),
            "image": imageName,
            "backups": bool(None),
            "ipv6": bool(False),
            'virtio': False,
            "private_networking": bool(None),
            "user_data": None,
        }
        json_params = json.dumps(data)
        r = requests.post('https://api.digitalocean.com/v2/droplets', data=json_params, headers=self.headers)
        droplet = Droplet(r.json()['droplet']['id'], name, r.json()['droplet']['status'])

        while(True):
            dr = self.retrieveDroplet(droplet.id)['droplet']
            if 'v4' in dr['networks'].keys() and len(dr['networks']['v4']) > 0:
                print "Get IP address: %s" % dr['networks']['v4'][0]['ip_address']
                # droplet.updateStatus(self)
                droplet.ip = dr['networks']['v4'][0]['ip_address']
                break
            else:
                print "Waiting for IP address"
                # print dr
                time.sleep(1)
                # droplet.updateStatus(self)
        print dr
        self.droplets.append(Droplet(**dr))
        self.ips.append(self.droplets[-1].ip)
        return dr


    def getSSHkeyID(self):
        res = list()
        r = requests.get("https://api.digitalocean.com/v2/account/keys", headers=self.headers)
        print r.headers['ratelimit-remaining']
        # print r.json()['ssh_keys'][0]['id']
        for id in r.json()['ssh_keys']:
            # print id['id']
            res.append(id['id'])
        # res.append(r.json()['ssh_keys'][0]['id'])
        print res
        return res

    def getDropletsList(self):
        res = []
        r = requests.get("https://api.digitalocean.com/v2/droplets", headers=self.headers)
        for droplet in r.json()['droplets']:
            res.append((droplet['id'], droplet['name'], droplet['networks']['v4'][0]['ip_address'], droplet['status']))
            # print droplet
            # if droplet['id'] not in [x.id for x in self.droplets]:
            #     self.droplets.append(Droplet(**droplet))
            #     self.ips.append(self.droplets[-1].ip)
            # print droplet['id'], droplet['name'], droplet['networks']['v4'][0]['ip_address'], droplet['status']
        return res

    def retrieveDroplet(self, dropletID):
        r = requests.get("https://api.digitalocean.com/v2/droplets/" + str(dropletID), headers=self.headers)
        # print r.content
        # print r.json()['droplet']['networks']['v4'][0]['ip_address']
        return r.json()

    def deleteDroplet(self, dropletID):
        r = requests.delete("https://api.digitalocean.com/v2/droplets/" + str(dropletID), params=None, headers=self.headers)
        print r.content

    def destorySSHKey(self, key_id):
        r = requests.delete("https://api.digitalocean.com/v2/account/keys/" + str(key_id), headers=self.headers)
        print r.content

    def createSSHKey(self, name, public_key_path):
        f = open(public_key_path, 'r')
        key = f.read()
        f.close()
        data = {
            "name": name,
            "public_key": key
        }
        json_params = json.dumps(data)
        r = requests.post("https://api.digitalocean.com/v2/account/keys", data=json_params, headers=self.headers)
        print r.content
        return r.json()['ssh_key']['id']

    def createInventory(self, key_file):
        key_file = os.path.abspath(key_file)
        f = open('inventory', 'r')
        text = f.read()
        f.close()
        f = open('inventory', 'ab')
        for droplet in [(x[0], x[2]) for x in self.getDropletsList()]:
            if droplet[1] not in text:
                s = '%d ansible_ssh_host=%s ansible_ssh_user=root ansible_ssh_private_key_file=%s' % (droplet[0], droplet[1], key_file,)
                print >> f, s
        # f.save()
        f.close()

    def checkIfAllActive(self):
        if all( [droplet[3] == 'active' for droplet in self.getDropletsList()]):
            return True
        else:
            return False

def main(argv):
    token = os.environ["DO_TOKEN"]
    conn = Digitalocean(token)
    if argv[1] == 'create':
        for i in range(argv[2]):
            print "--"
        print "hahah"
        # conn.createDroplet('devops3', 'nyc3', 'ubuntu-14-04-x32')
        # conn.createDroplet('devops3', 'nyc3', 'ubuntu-14-04-x32')
        # conn.createDroplet('devops3', 'nyc3', 'ubuntu-14-04-x32')
        # conn.createInventory(argv[2])
    print conn.getDropletsList()




if __name__ == "__main__":
    main(sys.argv)
# token = os.environ["DO_TOKEN"]
# conn = Digitalocean(token)


# conn.createDroplet('devops3', 'nyc3', 'ubuntu-14-04-x32')
# conn.createDroplet('devops3', 'nyc3', 'ubuntu-14-04-x32')
# conn.createDroplet('devops3', 'nyc3', 'ubuntu-14-04-x32')

# for droplet in conn.getDropletsList():
#     print droplet
#     conn.deleteDroplet(droplet[0])

# for line in conn.getDropletsList():
#     print line
# print conn.checkIfAllActive()
# conn.createInventory('private.key')
# conn.droplets[-1].checkStatus(conn)

# conn.createInventory('private.key')

# f = open('private.key', 'r')

# print os.path.abspath('private.key')
# createInventory('104.236.122.221', 'private.key')

# createSSHKey('devops', 'public.key', headers)

# getSSHkeyID(headers)
# print readKeyFile('public.key')
# destorySSHKey(headers, 1263300)
# createDroplet('devops2', 'nyc3', 'ubuntu-14-04-x32', headers)

# getDropletsList(headers)
# retrieveDroplet(headers, 7229651)
# deleteDroplet(headers, 7234669)
# listImages(headers)