from sensor import Sensor
import os
import subprocess
import signal
import datetime

class Network_sensor(Sensor):

    process = ""
    fpath = str(os.path.abspath('./network-analysis/bcc/tcpconnect.py'))
    output=""
    flagcsv = False
    directory=""

    def start(self):
        Network_sensor.process = subprocess.Popen(["python3", Network_sensor.fpath, "-o", self.output], shell=False)
        self.directory = str(self.output).replace(".","") + '/'
        #print("starting")
    
    def stop(self):
        p = self.process
        p.send_signal(signal.SIGINT)
        #outs, errs = p.communicate()
        #print('Terminate') 

    def get_files(self):
        resultPath = str(os.path.abspath('./'+'network-'+self.output))
        if self.flagcsv:
            print(resultPath)
        return resultPath
    
    #send formated data fo elasticsearch of the last created .csv
    def get_file(self):
        listfiles=os.listdir(self.directory)
        paths = [os.path.join(self.directory, basename) for basename in listfiles]
        last_file=max(paths, key=os.path.getctime)
        #print(last_file)
        with open(last_file,'r') as file :
            content=file.read()
            content = content.replace(" ","")
            tab = content.split(';')
            
        time=os.path.getmtime(last_file)
        timestamp='{:%Y-%m-%dT%H:%M:%S.%f%z}'.format(datetime.datetime.fromtimestamp(time))
        #print(timestamp)
        return {"Timestamp":timestamp,"PID":int(tab[0]),"Comm":tab[1],"Event":int(tab[2]),"SAddr":tab[3],"DAddr":tab[4],"DPort":int(tab[5].replace('\n',""))}