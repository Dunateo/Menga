#!/usr/bin/python
import sys
sys.path.append('./menga_cmdline')
from sensors_launch import start_sensors, stop_sensors, files_sensors, files_sensor_realtime
from docker_launch import docker_start, docker_stop, get_container_mainPid
from generate_report import generate_menga_report
from elastic_send import authent_es, save_es_stack
import argparse
import time

# arguments
examples = """examples:
    ./menga          #
    ./menga -dt      # duration time of the analysis
    ./menga -rt      # real time analysis
    ./menga -i       # specify docker image
    ./menga -csv     # dump at the end the raw csv files
    ./menga -o       # specify the output of the report cannot be used with -csv
"""
parser = argparse.ArgumentParser(
    description="Dynamic docker image analysis",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=examples)


parser.add_argument("-o", "--output", required=True,
    help="include the output name")
parser.add_argument("-csv", "--csv", action="store_true",
    help="dump all the sensor csv")
parser.add_argument("-i", "--image",
    help="include the docker image name")
parser.add_argument("-rt", "--realtime", action="store_true",
    help="realtime mode")
parser.add_argument("-dt", "--durationtime",
    help="duratime mode in seconds can't be use with rt")
parser.add_argument("-u", "--user",
    help="elastic user")
parser.add_argument("-p", "--pwd",
    help="elastic pass")
parser.add_argument("-ip", "--ip",
    help="elastic ip")
parser.add_argument("-id", "--index",
    help="elastic index")

args = parser.parse_args()

pid=""
did=""
container=""
es=""
print("Menga dynamic analysis for docker image")
print("---------------------------------------")
#Launch docker image
if args.image:
    try:
        container, did = docker_start(args.image)
        pid = int(get_container_mainPid(did))
    #container has not been init
    except TypeError:
        exit()



#Time Based Mode 
#real time 
if args.realtime and args.user and args.pwd and args.ip and args.index:
    try:
        es = authent_es(args.ip, '9200', args.user, args.pwd)
    except KeyboardInterrupt:
        exit()
    
    start_sensors(pid, args.output, args.csv)

    while True:
        try:
            data = files_sensor_realtime()
            save_es_stack(args.index, data, es)
        except KeyboardInterrupt:
            stop_sensors()
            docker_stop(container)
            exit()

#duration time
if args.durationtime:

    start_time = time.time()
    seconds = float(args.durationtime)
    start_sensors(pid, args.output, args.csv)

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        #break the loop 
        if elapsed_time >= seconds:
            print("Analysis duration: " + str(int(elapsed_time))  + " seconds")
            #sensors
            netpath, cpupath, kernelpath= files_sensors()
            stop_sensors()

            #report generation
            tab=(str(args.image),str(pid), str(int(elapsed_time)))
            generate_menga_report(str(args.output)+'.docx',tab, netpath, cpupath, kernelpath)
            
            #docker stop
            docker_stop(container)
            exit()

docker_stop(container)




