#Upload Files to CloudFiles
import pyrax
import time
import os.path

auth = pyrax.set_credential_file(os.path.expanduser("~/.rackspace_cloud_credentials"))
cloudfl = pyrax.cloudfiles

container_list = cloudfl.list_containers()

def get_dir_to_upload():
	direc = str(raw_input("Enter Directory to upload: "))
	return direc

#Create container - if non existent it will be created with builtin pyrax upload_folder
def create_and_upload(folder,container_name):
	if exists == True:
		upload_key, total_bytes = cloudfl.upload_folder(folder, container=container_name)
	else:
		upload_key, total_bytes = cloudfl.upload_folder(folder, container=container_name)
	return upload_key, total_bytes

# Check if directory exists
def check_if_dir_exist(dir):
	if os.path.exists(dir) == False or os.path.isdir(dir) == False:
		print "The %s directory does not exist or is not a directory, try again..." % dir
		return False
	else:
		print "Directory to upload found...Good..."
		return True

## Check Upload progress. Dividing Total bytes by progress to get percentage
def check_up_progress(upload_key,total_bytes):
	progress = 0
	while progress < total_bytes:
		progress = cloudfl.get_uploaded(upload_key)
		percent = ((progress * 100) / total_bytes)
		print percent, "% Uplodaded"
		time.sleep(5)

if __name__=="__main__":
	## Getting Directory to upoload from user
	print " Challenge 3: Write a script that accepts a directory as an argument as well as a container name. The script should upload the contents of the specified directory to the container (or create it if it doesn't exist). The script should handle errors appropriately. (Check for invalid paths, etc.) Worth 2 Points","\n"
	directory = get_dir_to_upload()
	exists = check_if_dir_exist(directory)

	## Loop until user inputs an existing directory
	while exists == False:
		directory = get_dir_to_upload()
		exists = check_if_dir_exist(directory)

	cont_name = str(raw_input("Now enter container name to use (If it does not exist it will be created) : "))

	up_key,upload_bytes = create_and_upload(directory,cont_name)

	upload_kbytes = float(upload_bytes) / 1024
	upload_mbytes = upload_kbytes / 1024
	upload_mbytes = float(upload_mbytes)

	print "Uploading %.2f MegaBytes" % upload_mbytes
	check_up_progress(up_key,upload_bytes)
	print "Upload Complete!"


