from flask import Flask
import webbrowser
import psutil
import os
import requests

app = Flask(__name__)

disk_partitions = psutil.disk_partitions()
for disk in disk_partitions:
    try:
        open(os.path.join(disk.mountpoint,".carnvial-app-drive")).read()
        os.listdir(os.path.join(disk.mountpoint,"carnivaldata"))
        break
    except:
        print("Drive not avalible")

@app.route('/')
def index():
    return 'Welcome to this website'

if __name__ == "__main__":
    webbrowser.open("http://localhost:6829")
    app.run(port="6829")
