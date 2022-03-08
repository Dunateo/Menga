import shutil
import os

#add content to a file 
def add_content(filename,content, mode):
    fname = "network-"+filename
    finalfile = open(fname, mode)
    finalfile.write(content)
    finalfile.close()

#delete complete directory with files
def delete_directory(path):
    try:
        shutil.rmtree(path)
    except OSError as e:
        print("Error on delete: %s : %s" % (path, e.strerror))


#create directory
def create_directory(path):
    try:
        os.mkdir(path)
    except OSError as e:
        print("Error on creation: %s : %s" % (path, e.strerror))