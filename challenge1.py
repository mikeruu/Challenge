import pyrax
import utils
import time
auth = pyrax.set_credential_file(".rackspace_cloud_credentials")
cloudsrv = pyrax.cloudservers
cloudlb = pyrax.cloud_loadbalancers

print "Challenge 1: Write a script that builds three 512 MB Cloud Servers that following a similar naming convention. (ie., web1, web2, web3) and returns the IP and login credentials for each server."
#create 2 servers and display their info
serv_name = "web"
num_servers = 2
imageid = "c195ef3b-9195-4474-b6f7-16e5bd86acd0"
flavor = 2

print "Three servers...coming right up!"

server_list = utils.create2servers(serv_name,imageid,flavor,num_servers)

for server in server_list:
	print "Server Name: ", server.name
	print "Server ID: ", server.id
	server_id = server.id
	print "Admin Pass: ",server.adminPass
	while not server.networks:
		time.sleep(5)
		server = cloudsrv.servers.get(server_id) 
	server_privip = server.networks["private"][0]
	server_pubip = server.networks["public"][0]
	server_ipv6 = server.networks["public"][1]
	#Insert Steps to add private ip to load balancer
	print "Private IP:",server_privip
	print  "Public IP:", server_pubip
	print "IPv6:", server_ipv6

print "DING!"

