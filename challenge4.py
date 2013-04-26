import pyrax
import pyrax.exceptions as exc
import time
import os.path
import re

auth = pyrax.set_credential_file(os.path.expanduser("~/.rackspace_cloud_credentials"))
clouddns = pyrax.cloud_dns


def isValidHostname(hostname):
	if len(hostname) > 255:
		return False
	if hostname[-1:] == ".":
		hostname = hostname[:-1] # strip exactly one dot from the right, if present
	allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
	return all(allowed.match(x) for x in hostname.split("."))

def check_ifdns_exists(zone):
	dns_list = clouddns.list() #get existing dns zones list
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
		
def add_dnsA_record(ip,ttl,domain):
	record = {
	        "type": "A",
	        "name": domain.name,
	        "data": ip,
	        "ttl": ttl,
	        }
	print "Adding A record"
	try:
 		record = domain.add_records(record)
	except exc.DomainRecordAdditionFailed:
		print "A Record aldready existed"
		return record
	except Exception as excp:
		print "Something went wrong"
		print excp
	else:
		print "A Record added: ",record
		return record


def main(hostname,email_add,ip,dom_ttl=600,rec_ttl=300):
	print "INPUT VALUES"
	print "######################################"
	print "Domain:", hostname
	print "Domain ttl:", dom_ttl,"secs"
	print "Email:",email_add
	print "IP Address for A record:", ip
	print "A record ttl:",rec_ttl,"secs"
	print "######################################"

	isValid = isValidHostname(hostname)
	dns_check,hostname_obj = check_ifdns_exists(hostname)


	if isValid == True and dns_check == False:
	#Create domain and add A record.
		#print "Domain is valid and Record does not exist"
		print "Creating domain.."
		try:
			domain = clouddns.create(name=hostname, emailAddress=email_add,
			        ttl=dom_ttl, comment="Domain")
		except Exception as excp:
			print "Error:",excp
		else:
			print "Domain Created Info: ",domain
			print "Now trying to add A record"
			a_record = add_dnsA_record(ip,rec_ttl,domain)
	elif isValid == True and dns_check == True:
		print "Domain is valid and already existed"
		a_record = add_dnsA_record(ip,rec_ttl,hostname_obj)
	#Create A record only
	else:
		print "Domain invalid"


## Logic - BEGIN - ##

if __name__=="__main__":
	print " Challenge 4: Write a script that uses Cloud DNS to create a new A record when passed a FQDN and IP address as arguments. Worth 1 Points\n"
	print "SET INPUT VALUES"
	hostname="sensorama.net"
	email_add="miguel@sensorama.net"
	ip = "166.78.62.40"
	dom_ttl = 600
	rec_ttl = 300
	main(hostname,email_add,ip)
	
		
