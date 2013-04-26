import utils
import pyrax
import time
import os.path

auth = pyrax.set_credential_file(os.path.expanduser("~/.rackspace_cloud_credentials"))
cloudsrv = pyrax.cloudservers.servers
cloudlb = pyrax.cloud_loadbalancers

def check_serv_networks(server_list):
	sample_server = server_list[-1] #Takea sample server to check on network build
	print "Servers created"
	print "waiting for networks to initialize.."
	#Will iterate if networks = null

	while not sample_server.networks:
			time.sleep(5)
			sample_server = cloudsrv.get(sample_server.id)
	print "Networks Initialized."
	return True		

def get_server_info(server_list): #Gets updated infomration from servers created that includes networks. Returns server_listnew and IP list
	print server_list
	server_listnew = [] #List 
	for serv in server_list:
	             server1 = cloudsrv.get(serv.id)
	             server_listnew.append(server1)
	#Get Private IPs from the new list and List useful server info
	ip_list = []
	count = 0 #pointer for reading server_list from the beginning
	for serv1 in server_listnew:
		ip_list.append(serv1.networks["private"][0])
		print "Node", serv1.name, "ID: ", serv1.id
		print "Public IP: ", serv1.networks["public"][0]
		print "Admin Pass: ", server_list[count].adminPass #Print Admin pass from the initial server_list
		count += 1
	return ip_list,server_listnew
		
def createlb_addnodes(ip_list,lb1_name):
	print "Creating nodes..."
	node_list = []
	for ip in range(len(ip_list)):#define nodes from ip_list
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
	return lb1,node_list

if __name__=="__main__":
	#Input from user or module
	print "Challenge 7: Write a script that will create 2 Cloud Servers and add them as nodes to a new Cloud Load Balancer.\n" 
	#lb1_name = raw_input("Enter Load Balancer Name:" )
	lb1_name = "peacekeeper"

	serv_name = "web"
	num_servers = 2
	imageid = "c195ef3b-9195-4474-b6f7-16e5bd86acd0"
	flavor = 2

	print "Creating Servers..."
	server_list = utils.create2servers(serv_name,imageid,flavor,num_servers) # missing utils. !!!!!!!!!!!!!!!!!!
	netalive = check_serv_networks(server_list)
	print netalive
	ip_list,server_listnew = get_server_info(server_list)
	lb1,node_list = createlb_addnodes(ip_list,lb1_name)









