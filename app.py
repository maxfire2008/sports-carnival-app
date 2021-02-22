from flask import Flask
import webbrowser
import psutil
import os

app = Flask(__name__)

disk_partitions = psutil.disk_partitions()
for disk in disk_partitions:
    try:
        open(os.path.join(disk.mountpoint,".carnvial-app-drive")).read()
        break
    except:
        print("Drive not avalible")

@app.route('/')
def index():
    return 'Welcome to this website'

if __name__ == "__main__":
    webbrowser.open("http://localhost:6829")
    app.run(port="6829")
