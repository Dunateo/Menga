from network_sensor import Network_sensor




net = Network_sensor()

#start all the sensors
def start_sensors(pid, output, csvflag):
    fonctions = ["Network_sensor"]
    
    #normal output
    net.output = output
    #csv flas
    if csvflag:
        net.flagcsv = True

    net.start()

#stop all the sensors
def stop_sensors():
    net.stop()
    
#get the files sensors
def files_sensors():
    return net.get_files() , "/home/valentin/Documents/Menga/perf.svg", "/home/valentin/Documents/Menga/kernel-result.csv"

def files_sensor_realtime():
    return net.get_file()
