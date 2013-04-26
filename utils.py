#!/usr/bin/python
# Filename: utils.py
import pyrax
import pyrax.exceptions as exc

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

def chkimgstatus(imagename,imageslist): #Check image status - return imglist.status
    imgstatus = 'UNKNOWN'
    for imglist in imageslist:
        if imglist.name == imagename:
           if imglist.status == 'SAVING':
                print 'SAVING'
                imgstatus = 'SAVING'
           elif imglist.status == 'ACTIVE':
                print 'Image Status: ACTIVE'
                imgstatus = 'ACTIVE'
           elif imglist.status == 'ERROR':
	            print 'ERROR'
	            imgstatus = 'ERROR'
           elif imglist.status == 'UNKNOWN':
	            print 'UNKNOWN'
	            imgstatus = 'UNKNOWN'
           elif imglist.status == 'DELETED':
	            print 'DELETED'
	            imgstatus = 'DELETED'
    return imglist.status, imglist.id

def chkimgeprogress(imagename): #Prints current server image progress
    progress = 0;
    imageslist = pyrax.cloudservers.images.list()
    for imglist in imageslist:
	    if imglist.name == imagename:
             return imglist.progress


def create2servers_net(srvname,imgid,flvr,num,networks):
	server_list = []
	i = 1 #start at 1 for the number on the name.
	num += 1
	while i < num:
		istr = str(i)
		srvname = str(srvname)
		server = pyrax.cloudservers.servers.create(srvname + istr ,imgid,flvr,nics=networks) 
		server_list.append(server)
		i += 1
	return server_list
	
def create_volumes(num_vols,vol_size,vol_name ="",vol_type="SATA",snap_id=""):
	vol_list = []
	print "Creating CBS Volumes"
	for num in range(num_vols):
		vol = pyrax.cloud_blockstorage.create(name=vol_name, size=vol_size, volume_type=vol_type , )
		vol_list.append(vol)
	return vol_list

version = '0.1'

def add_dns_record(rec_type,name,data,domain_obj):
	record_data = {"type": rec_type,"name": name,"data": data}
	rec_obj = [ ]
	print "Adding %s record" % rec_type
	try:
		record_obj = domain_obj.add_records(record_data)
	except exc.DomainRecordAdditionFailed as excp:
		print "Record aldready existed",excp
		rec_list = domain_obj.list_records()
		for rec in rec_list:
			if rec.name == name and rec.type == rec_type:
				print "Updating existing record..."
				rec.update(data=data)
	except Exception as excp:
		print "Something went wrong"
		print excp
	else:
		print "Record added: ",record_obj[0].name
		return record_obj

def check_ifdns_exists(zone):
	dns_list = pyrax.cloud_dns.list() #get existing dns zones list
	#get name list only
	zone_names = []
	for domain_zone in range(len(dns_list)): 
		znames = dns_list[domain_zone].name
		zone_names.append(znames) #get only the zone names on a list
	if zone in zone_names:
		return True,dns_list[domain_zone] #Provided zone already Exists
		print dns_list[domain_zone]
	else:
		return False,None #Provided Zone did not exist
		
# End of utils.py
