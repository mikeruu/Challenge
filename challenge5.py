import time
import pyrax
import json
import os

auth = pyrax.set_credential_file(".rackspace_cloud_credentials")

clouddb = pyrax.cloud_databases


inst_name = "challenge4"
inst_flavor = "m1.tiny"
inst_volume=2


inst = clouddb.create(inst_name, inst_flavor, inst_volume) #Create the instance
pyrax.utils.wait_until(inst, "status", "ACTIVE", interval=1, attempts=30, verbose=True)
print "after:",inst


inst_list = clouddb.list()
#print inst_list

for i in range(len(db_list)):
	print db_list[i]
#db_list[0]:
	
user = inst.create_user(name="user1", password="password", database_names=[challenge4])

for n in range(len(user)):
	print n," ",user[n]


	
#dbs = inst.list_databases()
users = inst.list_users()
#print "DBs:", dbs
print "Users:", users
#user = .create_user(name="groucho", password="top secret", database_names=[challenge4])
#print "User:", user	

	