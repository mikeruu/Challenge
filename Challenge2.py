#Create an image of a server
import pyrax
import time

auth = pyrax.set_credential_file("/Users/migu4903/project/.passwdfile")
cloudserv = pyrax.cloudservers

#imgname  = 'challenge2'

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

def chkimageprogress(imagename): #Prints current server image progress
    progress = 0;
    imageslist = cloudserv.images.list()
    for imglist in imageslist:
	    if imglist.name == imagename:
             return imglist.progress


serverid = raw_input("Please enter server id to image and clone: ")
clonename = raw_input("Clone Server Name: ")
imgname = raw_input("Enter name for image storage: ")
#serverid = '9413eff7-7f9b-43ea-9bec-b6c152f226a4'
print "Taking image from: ", serverid


cloudserv.servers.create_image(serverid,imgname) #Create image from serverid
imgslist = cloudserv.images.list()
imgstatus, imgid = chkimgstatus(imgname,imgslist)

imageprogress = 0;
while imageprogress < 99: #Loop to display image progress
    imageprogress = chkimageprogress(imgname)
    print imageprogress, '% Image - Not Ready'
    time.sleep(10)
   
print imageprogress, '% Image - Process Completed'
imgstatus, imgid = chkimgstatus(imgname,imgslist)
print "Result Image ID: ", imgid	  
if imgstatus == 'ACTIVE':	
    clone = pyrax.cloudservers.servers.create(clonename,imgid,2)
    print "Server Created"
    print "Server Name: ", clonename
    print "Admin Pass: ", clone.adminPass
    print "Server ID: ", clone.id
else:
	print "Image status is not ACTIVE"
	print "Current Status: ", imgstatus