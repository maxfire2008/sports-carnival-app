import flask
import webbrowser
import psutil
import os
import requests
import time
import base64

app = flask.Flask(__name__)

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
    return 'Welcome to this website it so far does nothing!'
@app.route('/entertestrace',methods = ['POST'])
def entertestrace():
    data = flask.request.form['d']
    filename = base64.urlsafe_b64encode(str(time.time()).encode()[-8:]+os.urandom(4)).decode()
    with open(os.path.join(disk.mountpoint,"carnivaldata",filename+".crn"),"w+") as savefile:
        savefile.write(data)
        savefile.close()
    return os.path.join(disk.mountpoint,"carnivaldata",filename+".crn")

if __name__ == "__main__":
##    webbrowser.open("http://localhost:6829")
    app.run(port="6829",host="localhost",debug=True)
