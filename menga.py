#!/usr/bin/python
import sys
sys.path.append('./menga_cmdline')
from sensors_launch import start_sensors, stop_sensors, files_sensors
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


parser.add_argument("-o", "--output",
    help="include the output name")
parser.add_argument("-csv", "--csv", action="store_true",
    help="dump all the sensor csv")
parser.add_argument("-i", "--image",
    help="include the docker image name")
parser.add_argument("-rt", "--realtime", action="store_true",
    help="realtime mode")
parser.add_argument("-dt", "--durationtime",
    help="duratime mode in seconds")


args = parser.parse_args()

if args.output:
    print("output option")

if args.csv:
    print("csv option")

if args.image:
    print(args.image)



#Time Based Mode 
#real time 
if args.realtime:

    while True:
        try:
            print("not ctlc")
        except KeyboardInterrupt:
            print("Bye tl+c")
            exit()

#duration time
if args.durationtime:

    start_time = time.time()
    seconds = float(args.durationtime)
    start_sensors("3704", args.output)

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
    
        if elapsed_time >= seconds:
            print("Analysis duration: " + str(int(elapsed_time))  + " seconds")
            files_sensors()
            stop_sensors()
            exit()
