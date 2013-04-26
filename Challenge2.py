#Create an image of a server
import pyrax
import time
import utils
import os.path
import pyrax.exceptions as exc
import novaclient.exceptions
import sys

auth = pyrax.set_credential_file(os.path.expanduser("~/.rackspace_cloud_credentials"))
cloudserv = pyrax.cloudservers

#imgname  = 'challenge2'
print "Challenge 2: Write a script that clones a server (takes an image and deploys the image as a new server). Worth 2 Points\n"
serverid = raw_input("Please enter server id to image and clone: ")
clonename = raw_input("Clone Server Name: ")
imgname = raw_input("Enter name for image storage: ")
#serverid = '9413eff7-7f9b-43ea-9bec-b6c152f226a4'
print "Taking image from: ", serverid

try:
	cloudserv.servers.create_image(serverid,imgname) #Create image from serverid
except novaclient.exceptions.NotFound as excp:
	print excp
	sys.exit(0)

imgslist = cloudserv.images.list()
imgstatus, imgid = utils.chkimgstatus(imgname,imgslist)

imageprogress = 0;
while imageprogress < 99: #Loop to display image progress
    imageprogress = utils.chkimgeprogress(imgname)
    print imageprogress, '% Image - Not Ready'
    time.sleep(10)
   
print imageprogress, '% Image - Process Completed'
imgstatus, imgid = utils.chkimgstatus(imgname,imgslist)
print "Result Image ID: ", imgid	  
if imgstatus == 'ACTIVE':	
    clone = utils.create1server(clonename,imgid,2)
    print "Server Created"
    print "Server Name: ", clonename
    print "Admin Pass: ", clone.adminPass
    print "Server ID: ", clone.id
else:
	print "Image status is not ACTIVE"
	print "Current Status: ", imgstatus