from tkinter import *
from tkinter import ttk
from typing import Container

import docker
import psutil

import os
import sys

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from PIL import Image, ImageTk

from functools import partial

# Function to print the process list of the selected docker
def list_process_docker(docker_list: Listbox, container_list: any, process_list: Listbox):
    process_list.delete(0, END)
    line = docker_list.curselection()[0]
    total = container_list[line].top()
    cpt = 0
    for x in total["Processes"]:
        cpt += 1
        process_list.insert(END, str(cpt) + ". [PID] " + str(x[1]) + " ; [CMD] " + str(x[7]))

# Function to analyze the cpu usage of the selected docker
def start_cpu_analysis():
    print("Starting CPU analysis")

# Function to analyze the selected network interface
def start_network_analysis():
    print("Starting network analysis")

# Function to analyze the current process of the selected docker
def start_process_analysis():
    print("Starting process analysis")

# Function to refresh the docker list
def refresh_docker_list(docker_list: Listbox, cli: docker.DockerClient):
    print("Refreshing docker list")
    docker_list.delete(0, END)
    containers = cli.containers.list()
    cpt = 0
    for x in containers:
        cpt += 1
        docker_list.insert(END, str(cpt) + ". [NAME] " + x.name + " ; [ID] " + x.short_id)

# Function to refresh the process list
def refresh_process_list(docker_list: Listbox, cli: docker.DockerClient, process_list: Listbox):
    process_list.delete(0, END)
    refresh_docker_list(docker_list, cli)

# Function to refresh the network interface list
def refresh_network_interface_list(network_interface_list: Listbox, cli: docker.DockerClient):
    print("Refreshing network interface list")
    network_interface_list.delete(0, END)
    addrs = psutil.net_if_addrs()
    cpt = 0
    for x in addrs.keys():
        cpt += 1
        network_interface_list.insert(END, str(cpt) + ". " + x)

# Function to refresh if docker is running
def refresh_error(error_window: Tk):
    if check_docker():
        print("Docker is running now")
        # Destroy the error window
        error_window.destroy()
        # Create the main window
        create_main_window()
    else:
        print("Docker still not running")

# Function to check if docker is running
def check_docker():
    docker_state=0
    for process in psutil.process_iter():
        if process.name() == "docker":
            docker_state += 1
        else:
            docker_state += 0

    if docker_state == 0:
        return FALSE
    else:
        return TRUE

def create_main_window():
    # Creating the main window
    main_window = Tk()
    # Defining the window's title
    main_window.title("Menga")
    # Creating the tab's system
    n = ttk.Notebook(main_window)
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

    ################################
    ####### CPU Analysis Tab #######
    ################################

    # Shared variable
    selected_docker = StringVar()

    # Docker List Frame
    docker_list_frame = LabelFrame(o1, text="Docker list", height=200, padx=20, pady=20)
    docker_list_frame.pack(fill="both", expand="yes")

    # Listing running docker
    cli = docker.DockerClient()
    containers = cli.containers.list()

    # Listbox of running docker
    docker_list = Listbox(docker_list_frame, width=50, height=20)
    cpt = 0
    for x in containers:
        cpt += 1
        docker_list.insert(END, str(cpt) + ". [NAME] " + x.name + " ; [ID] " + x.short_id)
    docker_list.pack()

    # Refresh Button
    refresh_button_docker = Button(docker_list_frame, text="Refresh", command=partial(refresh_docker_list, docker_list, cli))
    refresh_button_docker.pack()

    # Start Button
    start_button_cpu = Button(docker_list_frame, text="Start", command=start_cpu_analysis)
    start_button_cpu.pack()

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
    refresh_button_network = Button(network_interface_list_frame, text="Refresh", command=partial(refresh_network_interface_list, network_interface_list, cli))
    refresh_button_network.pack()

    # Start Button
    start_button_network = Button(network_interface_list_frame, text="Start", command=start_network_analysis)
    start_button_network.pack()

    ####################################
    ####### Process Analysis Tab #######
    ####################################

    selected_docker :Container = None

    # Docker List Frame
    docker_list_frame = LabelFrame(o3, text="Docker list", padx=20, pady=20)
    docker_list_frame.pack(fill="both", expand="yes")

    # Listing running docker
    cli = docker.DockerClient()
    containers = cli.containers.list()

    # Listbox of running docker
    docker_list = Listbox(docker_list_frame, width=60, height=10)
    cpt = 0
    for x in containers:
        cpt += 1
        docker_list.insert(END, str(cpt) + ". [NAME] " + x.name + " ; [ID] " + x.short_id)
    docker_list.pack()

    # Process List Frame
    process_list_frame = LabelFrame(o3, text="Process list", padx=20, pady=20)

    # Listbox of running docker
    process_list = Listbox(process_list_frame, width=60, height=30)

    # Refresh Button
    refresh_button_docker = Button(docker_list_frame, text="Refresh", command=partial(refresh_process_list, docker_list, cli, process_list))
    refresh_button_docker.pack()

    # Check Button
    check_button_docker = Button(docker_list_frame, text="Check", command=partial(list_process_docker, docker_list, containers, process_list))
    check_button_docker.pack()

    # Place Process List Frame
    process_list_frame.pack(fill="both", expand="yes")

    # Place Listbox of processes of one running docker
    process_list.pack()

    # Start Button
    start_button_process = Button(process_list_frame, text="Start", command=start_process_analysis)
    start_button_process.pack()

     # Display main window
    main_window.mainloop()
    

######################
#### Error Window ####
######################

def create_error_window():
    # Creating the error window
    error_window = Tk()
    # Defining the error window's title
    error_window.title("Menga : ERROR[Docker is not running]")
    # Defining the error window's size
    error_window.geometry("364x364")
    # Error Label
    error_label = Label(error_window, text="Docker is not running !")
    error_label.pack()
    error_label.place(relx=.5, rely=.4, anchor="center")
    # Refresh Button
    refresh_button_error = Button(error_window, text="Refresh", command=partial(refresh_error, error_window))
    refresh_button_error.pack()
    refresh_button_error.place(relx=.5, rely=.5, anchor="center")
    # Display error window
    error_window.mainloop()


if check_docker():
    # Creating the main window
    create_main_window()
else:
    create_error_window()
