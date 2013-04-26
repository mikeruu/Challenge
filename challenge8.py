import pyrax
import time
import os.path
import challenge6
import challenge4
import utils
import pyrax.exceptions as exc

clouddns = pyrax.cloud_dns
auth = pyrax.set_credential_file(os.path.expanduser("~/.rackspace_cloud_credentials"))
cloudsrv = pyrax.cloudservers.servers
cloudlb = pyrax.cloud_loadbalancers
cloudfiles = pyrax.cloudfiles
cloudnet = pyrax.cloud_networks
cloudcbs = pyrax.cloud_blockstorage
clouddns = pyrax.cloud_dns

print "Challenge 8: Write a script that will create a static webpage served out of Cloud Files. The script must create a new container, cdn enable it, enable it to serve an index file, create an index file object, upload the object to the container, and create a CNAME record pointing to the CDN URL of the container. Worth 3 Points"
print '#'* 50

if __name__=="__main__":
	print "Input Values:"
	print " cont_name = challenge8\n \
index_page = <html><body>Index Page</body></html>\n \
domain_name = sensorama.net\n \
rec_type = CNAME\n \
rec_name = www.sensorama.net\n \
ttl = 300\n \
email_add = miguel@sensorama.net"
	
	
	cont_name = "challenge8"
	index_page = "<html><body>Index Page</body></html>"
	domain_name = "sensorama.net"
	rec_type = "CNAME"
	rec_name = "www.sensorama.net"
	ttl = 300
	email_add = "miguel@sensorama.net"

	
	cont_obj = challenge6.main(cont_name)
	print "Index Page Set.."
	obj = cloudfiles.store_object(cont_name, "index.html", index_page)
	cont_obj.set_web_index_page(index_page)
	cont = cloudfiles.get_container(cont_name)
	uri = cont.cdn_uri
	uri = uri.translate(None, 'http://')
	
	dns_exists,domain_obj = utils.check_ifdns_exists(domain_name)
	
	if dns_exists == False:
	#Create domain and add A record.
		#print "Domain Record does not exist"
		print "Creating domain.."
		try:
			domain_obj = clouddns.create(name=domain_name, emailAddress=email_add,
			        ttl=ttl, comment="Domain")
		except Exception as excp:
			print "Error:",excp
		else:
			print "Domain Created Info: ",domain_obj	
	record = utils.add_dns_record(rec_type,rec_name,uri,domain_obj)
	print "Done"
		
