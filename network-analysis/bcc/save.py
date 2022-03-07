
#add content to a file 
def add_content(filename,content, mode):
    finalfile = open(filename, mode)
    finalfile.write(content)
    finalfile.close()


