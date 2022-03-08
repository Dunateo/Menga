import docker
import subprocess

def docker_start(image_name):
    try:
        client = docker.from_env()
        container = client.containers.run(str(image_name), detach=True)
        print("start docker container with the img",image_name)
        #print(str(client.containers.list()))
        return container, container.id
    except Exception:
        print("Error launching container")
        

def docker_stop(container):
    container.stop()
    print("Container Docker has been stop")

def get_container_mainPid(did):

    result = subprocess.run(["docker","inspect","-f", "'{{.State.Pid}}'", did], stdout=subprocess.PIPE)
    pid = result.stdout.decode('utf-8')
    pid = pid.strip('\n')
    return pid.replace("'","")