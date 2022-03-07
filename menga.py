#!/usr/bin/python
import argparse

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
parser.add_argument("-csv", "--csv",
    help="dump all the sensor csv")
parser.add_argument("-i", "--image",
    help="include the docker image name")
parser.add_argument("-rt", "--realtime",
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

if args.realtime:
    print(args.realtime)

if args.durationtime:
    print(args.durationtime)
