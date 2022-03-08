from sensor import Sensor
import os
import subprocess
import signal

class Network_sensor(Sensor):

    process = ""
    fpath = str(os.path.abspath('./network-analysis/bcc/tcpconnect.py'))
    output=""
    flagcsv = False

    def start(self):
        Network_sensor.process = subprocess.Popen(["python3", Network_sensor.fpath, "-o", self.output], shell=False)
        print("starting")
    
    def stop(self):
        p = self.process
        p.send_signal(signal.SIGINT)
        #outs, errs = p.communicate()
        print('Terminate') 

    def get_files(self):
        resultPath = str(os.path.abspath('./'+self.output))
        if self.flagcsv:
            print(resultPath)
        return resultPath