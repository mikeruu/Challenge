import pyrax
import utils
import time

auth = pyrax.set_credential_file(".rackspace_cloud_credentials")
cloudsrv = pyrax.cloudservers.servers
cloudlb = pyrax.cloud_loadbalancers


#Input from user or module
print "Challenge 7: Write a script that will create 2 Cloud Servers and add them as nodes to a new Cloud Load Balancer." 
#lb1_name = raw_input("Enter Load Balancer Name:" )
lb1_name = "peacekeeper"

#Get server list
serv_name = "web"
num_servers = 2
imageid = "c195ef3b-9195-4474-b6f7-16e5bd86acd0"
flavor = 2

print "Creating Servers..."
server_list = utils.create2servers(serv_name,imageid,flavor,num_servers)

#Takea sample to check on networks
sample_server = server_list[0]
#Will iterate if networks = null
print "Servers created"
print "waiting for networks to initialize.."
while not sample_server.networks:
		time.sleep(5)
		sample_server = cloudsrv.get(sample_server.id)
print "Networks Initialized."		
#Get new infomration from servers
server_listnew = [] #List 
for serv in server_list:
             server1 = cloudsrv.get(serv.id)
             server_listnew.append(server1)

#Get Private IPs from the new list and List useful server info
ip_list = []
count = 0 #pointer for reading server_list from the beginning
for serv1 in server_listnew:
	ip_list.append(serv1.networks["public"][0])
	print "Node:"+count, serv1.name, "ID: ", serv1.id
	print "Public IP: ", serv1.networks[]
	print "Admin Pass: ", server_list[count].adminPass
	count += 1
		
#define nodes from ip_list
print "Creating nodes..."
node_list = []
for ip in range(len(ip_list)):
	node_list.append(cloudlb.Node(address=ip_list[ip], port=80, condition="ENABLED"))
	
#Create Public ip of lb
pub_ip = cloudlb.VirtualIP(type="PUBLIC")

#Create LB and add nodes under port 80
print "Creating LB and adding nodes"
lb1 = cloudlb.create(lb1_name, port=80, protocol="HTTP",
        nodes=node_list, virtual_ips=[pub_ip])
print "Load Balancer Information"
print "ID: ", lb1.id
print "Public IPv4: ", lb1.sourceAddresses["ipv4Public"]














