from tkinter import *
from tkinter import ttk
import docker
import psutil
import os
import psutil
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from PIL import Image, ImageTk

# Function to refresh the docker list
def refresh_docker_list():
    docker_list.delete(0, END)
    containers = cli.containers.list()
    cpt = 0
    for x in containers:
        cpt += 1
        docker_list.insert(END, str(cpt) + ". " + x.name + " : " + x.short_id)

# Function to refresh the network interface list
def refresh_network_interface_list():
    network_interface_list.delete(0, END)
    addrs = psutil.net_if_addrs()
    cpt = 0
    for x in addrs.keys():
        cpt += 1
        network_interface_list.insert(END, str(cpt) + ". " + x)

# Function to refresh the process list
def refresh_process_list():
    print("Refreshing list")

# Creating the main window
fenetre = Tk()
# Defining the window's dimensions
# fenetre.geometry("1024x768")
# Defining the window's title
fenetre.title("Menga")

# Creating the tab's system
n = ttk.Notebook(fenetre)
n.pack()
# Adding CPU Analysis tab
o1 = ttk.Frame(n)
o1.pack()
# Adding Network Analysis tab
o2 = ttk.Frame(n)
o2.pack()
# Adding Process Analysis tab
o3 = ttk.Frame(n)
o3.pack()
# Tab CPU Analysis name
n.add(o1, text='CPU Analysis')
# Tab Network Analysis name
n.add(o2, text='Network Analysis')
# Tab Process Analysis name
n.add(o3, text='Process Analysis')

# Exemple
label = Label(o3, text="Hello World")
label.pack()

################################
####### CPU Analysis Tab #######
################################

# Check if Docker is running
processlist=list()
docker_state=0
for process in psutil.process_iter():
    if process.name() == "dockerd":
        docker_state += 1
    else:
        docker_state += 0

if docker_state == 0:
    print("Docker is not running")
else:
    print("Docker is running")

# Docker List Frame
docker_list_frame = LabelFrame(o1, text="Docker list", padx=20, pady=20)
docker_list_frame.pack(fill="both", expand="yes")

cli = docker.DockerClient()
containers = cli.containers.list()

docker_list = Listbox(docker_list_frame, width=50, height=20)
cpt = 0
for x in containers:
    cpt += 1
    docker_list.insert(END, str(cpt) + ". " + x.name + " : " + x.short_id)
docker_list.pack()

# Refresh Button
refresh_Button = Button(docker_list_frame, text="Refresh", command=refresh_docker_list)
refresh_Button.pack()

# Last Analysis Frame
# Looking for a svg file
path = "./CPU_Analysis/"
cpt = 0

for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".svg"):
            cpt += 1
            file = os.path.join(root, file)
            print(os.path.join(root, file))
            drawing = svg2rlg(file)
            renderPM.drawToFile(drawing, "./temp.png", fmt="PNG")
            img = Image.open('./temp.png')
            pimg = ImageTk.PhotoImage(img)
            size = img.size
            cpu_analysis_frame = LabelFrame(o1, text="Last Analysis Result", padx=1, pady=20)
            cpu_analysis_frame.pack(fill="both", expand="yes")
            image_frame = Canvas(cpu_analysis_frame, width=700, height=500, scrollregion=(0,0,500,500))
            hbar=Scrollbar(cpu_analysis_frame,orient=HORIZONTAL)
            hbar.pack(side=BOTTOM,fill=X)
            hbar.config(command=image_frame.xview)
            vbar=Scrollbar(cpu_analysis_frame,orient=VERTICAL)
            vbar.pack(side=RIGHT,fill=Y)
            vbar.config(command=image_frame.yview)
            image_frame.config(width=700,height=500)
            image_frame.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
            image_frame.create_image(0,0,anchor='nw',image=pimg)
            image_frame.pack(expand=True,fill=BOTH)

if cpt == 0:
    print("No svg file found")
else:
    print("Found " + str(cpt) + " svg file")



####################################
####### Network Analysis Tab #######
####################################

# Network Interface List Frame
network_interface_list_frame = LabelFrame(o2, text="Interface list", padx=20, pady=20)
network_interface_list_frame.pack(fill="both", expand="yes")

addrs = psutil.net_if_addrs()

network_interface_list = Listbox(network_interface_list_frame, width=50, height=20)
cpt = 0
for x in addrs.keys():
    cpt += 1
    network_interface_list.insert(END, str(cpt) + ". " + x)
network_interface_list.pack()

# Refresh Button
refresh_Button = Button(network_interface_list_frame, text="Refresh", command=refresh_network_interface_list)
refresh_Button.pack()


####################################
####### Process Analysis Tab #######
####################################


fenetre.mainloop()