import pyrax
import time
import os.path
import challenge7
import challenge4

auth = pyrax.set_credential_file(os.path.expanduser("~/.rackspace_cloud_credentials"))
cloudsrv = pyrax.cloudservers.servers
cloudlb = pyrax.cloud_loadbalancers
cloudfiles = pyrax.cloudfiles

def create2servers_file(srvname,imgid,flvr,num,file):
	server_list = []
	i = 1 #start at 1 for the number on the name.
	num += 1
	while i < num:
		istr = str(i)
		srvname = str(srvname)
		server = pyrax.cloudservers.servers.create(srvname + istr ,imgid,flvr,files=file) 
		server_list.append(server)
		i += 1
	return server_list


if __name__=="__main__":
	
	print "Write an application that will: \
	- Create 2 servers, supplying a ssh key to be installed at /root/.ssh/authorized_keys. \
	- Create a load balancer \
	- Add the 2 new servers to the LB \
	- Set up LB monitor and custom error page. \
	- Create a DNS record based on a FQDN for the LB VIP. \
	- Write the error page html to a file in cloud files for backup.\n "
	
	authorized_keys = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC2iUtOmliAQplsYGc4jli1Q0X1m3JD2LV/v6glaBb1dvCnC4qxxzMFHau0qjyv8fHpf3lYyFR3tlgEcI7y42k4MNp/ZRC7IPOg7dsndB1BMyQ7WKYBCyv5puLQ3bNXLJJWRzOELQPrWJ1b1RhrQHMgGMEUbsE/KxT7H+VgfbBMjwTKd1sceddPv3YUpzX11SUAn4FoABS8rQunNY6qc5uZ+wZ7+ztREEmquoPyamb9kYzijtEfP0j/K/4p4SDsBkFQWI5EVHKQCAw6p/7K+Lmf4C/3J+Pf17VdrVD7EAoctC+XXZBTRqFleMo1imQIQxeq5huO2p/HTFr41A9pFCOr root@MG9KHBDRJ7"

	serv_name = "web"
	imageid = "c195ef3b-9195-4474-b6f7-16e5bd86acd0"
	flavor = 2
	num_servers = 2
	lb1_name = "peacekeeper"
	dns_zone = "sensorama.net"
	email_add = "miguel@sensorama.net"
	cont_name = "project"
	error_page = "<html><body>Custom Error Page</body></html>"
	file = {"/root/.ssh/authorized_keys":authorized_keys}


	#create two servers
	print "Creating two servers with file injection"
	server_list = create2servers_file(serv_name,imageid,flavor,num_servers,file)
	network_avail = challenge7.check_serv_networks(server_list)
	print "Server List: ",server_list
	time.sleep(3)
	ip_list,server_listnew = challenge7.get_server_info(server_list)
	print "Creating Load Balancer and adding nodes"
	lb1,node_list = challenge7.createlb_addnodes(ip_list,lb1_name)
	pyrax.utils.wait_until(lb1, "status", "ACTIVE", interval=3, attempts=30, verbose=True)
	print "LB DONE..ADDING monitoring"	
	time.sleep(2)
	lb1.add_health_monitor(type="CONNECT", delay=10, timeout=10,
	        attemptsBeforeDeactivation=3)
	pyrax.utils.wait_until(lb1, "status", "ACTIVE", interval=3, attempts=30, verbose=True)
	print "Setting custom error page"
	lb1.set_error_page(error_page)
	pyrax.utils.wait_until(lb1, "status", "ACTIVE", interval=3, attempts=30, verbose=True)
	print "Creating DNS Record"
	challenge4.main(dns_zone,email_add,lb1.sourceAddresses["ipv4Public"])
	print "Creating container"
	cont_obj = cloudfiles.create_container(cont_name)
	print "Backing up file to Cloud Files"
	obj = cloudfiles.store_object(cont_name, "error_page.html", error_page)	
	
		