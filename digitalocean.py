import requests
import json

token = '36a1f584c52b6b9d38ed917d4ccea312b6e13de7325652b1cdf806353deb07c1'

headers = {
	'Authorization': 'Bearer ' + token,
	'Content-Type': 'application/json'
}

def listRegions(headers):
	r = requests.get("https://api.digitalocean.com/v2/regions", headers=headers)
	for region in r.json()['regions']:
		print region['slug']


def listImages(headers):
	r = requests.get("https://api.digitalocean.com/v2/images", headers=headers)
	for image in r.json()['images']:
		print image['slug']


def createDroplet(name, region, imageName, headers):
	data = {
			"name": name,
			"region":region,
			"size":"512mb",
			"ssh_keys":[1263300],
			"image":imageName,
			"backups":bool(None),
			"ipv6":bool(False),
			'virtio': False,
			"private_networking":bool(None),
			"user_data": None,
		}
	json_params = json.dumps(data)
	r = requests.post('https://api.digitalocean.com/v2/droplets', data=json_params, headers=headers)
	# print json_params
	print r.content

def getSSHkeyID(headers):
	res = list()
	r = requests.get("https://api.digitalocean.com/v2/account/keys", headers=headers)
	# print r.json()['ssh_keys'][0]['id']
	res.append(r.json()['ssh_keys'][0]['id'])
	print res
	return res

def getDropletsList(headers):
	r = requests.get("https://api.digitalocean.com/v2/droplets", headers=headers)
	for droplet in r.json()['droplets']:
		print droplet['id'], droplet['name']

def retrieveDroplet(headers, dropletID):
	r = requests.get("https://api.digitalocean.com/v2/droplets/" + str(dropletID), headers=headers)
	print r.json()['droplet']['networks']['v4'][0]['ip_address']

def deleteDroplet(headers, dropletID):
	r = requests.delete("https://api.digitalocean.com/v2/droplets/" + str(dropletID), params=None, headers=headers)
	print r.content

# getSSHkeyID(headers)
# createDroplet('Test2', 'nyc3', 'ubuntu-15-04-x32', headers)

# getDropletsList(headers)
# retrieveDroplet(headers, 7229651)
deleteDroplet(headers, 7229651)
# listImages(headers)