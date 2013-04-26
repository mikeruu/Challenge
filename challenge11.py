import pyrax
import time
import os.path
import challenge7
import challenge4
import utils

auth = pyrax.set_credential_file(os.path.expanduser("~/.rackspace_cloud_credentials"))
cloudsrv = pyrax.cloudservers.servers
cloudlb = pyrax.cloud_loadbalancers
cloudfiles = pyrax.cloudfiles
cloudnet = pyrax.cloud_networks
cloudcbs = pyrax.cloud_blockstorage

def attach_cbs_2servers(server_list,vol_list,mntpoint):
	for obj in range(len(server_list)):
		server = server_list[obj]
		volume = vol_list[obj]
		volume.attach_to_instance(server, mountpoint= mntpoint)
	print "CBS Volumes Attached.."


if __name__=="__main__":

	serv_name = "web"
	imageid = "c195ef3b-9195-4474-b6f7-16e5bd86acd0"
	flavor = 2
	num_servers = 3
	priv_network = "192.168.0.0"
	priv_net_name = "admin_network"
	vol_size = 100
	mntpoint = "/dev/xvdb"
	lb1_name = "peacekeeper"
	dns_zone = "sensorama.net"
	email_add = "miguel@sensorama.net"

	priv_network = priv_network + "/24" #Add subnetmask
	print "Creating Cloud Network:", priv_net_name
	network = cloudnet.create(priv_net_name, cidr=priv_network)
	networks = network.get_server_networks(public=True, private=True)
	time.sleep(10)
	vol_list = utils.create_volumes(num_servers,vol_size)
	print "New Cloud Network:", network.cidr
	print "Creating servers....."
	server_list = utils.create2servers_net(serv_name,imageid,flavor,num_servers,networks)
	netalive = challenge7.check_serv_networks(server_list)
	pyrax.utils.wait_until(server_list[-1], "status", "ACTIVE", interval=5, attempts=40, verbose=True)

	ip_list,server_listnew = challenge7.get_server_info(server_list)
	lb1,node_list = challenge7.createlb_addnodes(ip_list,lb1_name)

	challenge4.main(dns_zone,email_add,lb1.sourceAddresses["ipv4Public"])
	attach_cbs_2servers(server_list,vol_list,mntpoint)

