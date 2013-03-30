#!/usr/bin/python
# Filename: utils.py
import pyrax
#Cloudservers Utils
def create1server(srvname,imgid,flvr):
    server = pyrax.cloudservers.servers.create(srvname,imgid,flvr)
    return server

def create2servers(srvname,imgid,flvr,num):
	server_list = []
	i = 1 #start at 1 for the number on the name.
	num += 1
	while i < num:
		istr = str(i)
		srvname = str(srvname)
		server = pyrax.cloudservers.servers.create(srvname + istr ,imgid,flvr) 
		server_list.append(server)
		i += 1
	return server_list







version = '0.1'

# End of utils.py
