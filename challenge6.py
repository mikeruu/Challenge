import pyrax
import time
import os.path

auth = pyrax.set_credential_file(os.path.expanduser("~/.rackspace_cloud_credentials"))
cloudfl = pyrax.cloudfiles

def main(cont_name):
	cont_list = cloudfl.list_containers()
	#print "list_containers:", cont_list

	if cont_name in cont_list:
		print "Container already exists.. only enabling CDN Support"
	else:
		print "Creating container with CDN support"
			
	cont = cloudfl.create_container(cont_name)
	cloudfl.make_container_public(cont_name, ttl=900)
			
	print "Container:",cont.name
	print "CDN Enabled:", cont.cdn_enabled
	return cont

if __name__=="__main__":
	
	print "Challenge 6: Write a script that creates a CDN-enabled container in Cloud Files. Worth 1 Point\n"
	cont_name = str(raw_input("Please enter the name of the CDN Container to create: "))
	container = main(cont_name)
	#cont_name = "cdn_cont3"
	
