from sensor import Sensor
import os
import subprocess

class Network_sensor(Sensor):

    process = ""
    fpath = str(os.path.abspath('../network-analysis/bcc/tcpconnect.py'))
    output=""

    def start(self):
        Network_sensor.process = subprocess.Popen(["python3", Network_sensor.fpath, "--output", Network_sensor.output], shell=False)
        print("starting")
    
    def stop(self):
        p = Network_sensor.process
        p.kill()
        outs, errs = p.communicate()
        print('Terminate') 

    def get_files(self):
        resultPath = str(os.path.abspath('../network-analysis/bcc/'+Network_sensor.output))
        print("get files")
        return resultPath