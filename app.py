import flask
import webbrowser
import psutil
import os
import requests
import time
import base64
import tempfile
import shutil

app = flask.Flask(__name__)

def checkfoldersandcreate():
    tmpdir = tempfile.gettempdir()
    try:
        os.listdir(os.path.join(tmpdir,"carnivaldata"))
    except:
        os.mkdir(os.path.join(tmpdir,"carnivaldata"))
    try:
        os.listdir(os.path.join(tmpdir,"carnivaldata","clientoutgoing"))
    except:
        os.mkdir(os.path.join(tmpdir,"carnivaldata","clientoutgoing"))
    try:
        os.listdir(os.path.join(tmpdir,"carnivaldata","clientincoming"))
    except:
        os.mkdir(os.path.join(tmpdir,"carnivaldata","clientincoming"))
checkfoldersandcreate()
        
def getdisk():
    disk_partitions = psutil.disk_partitions()
    for disktosearch in disk_partitions:
        try:
            open(os.path.join(disktosearch.mountpoint,".carnival-app-drive")).read()
            os.listdir(os.path.join(disktosearch.mountpoint,"carnivaldata"))
            break
        except:
            print("Drive not avalible")
            disktosearch = None
    return disktosearch

def syncdata():
    disk = getdisk()
    if disk:
        tmpdir = os.path.join(tempfile.gettempdir(),"carnivaldata")
        diskdir = os.path.join(disk.mountpoint,"carnivaldata")
        for file in os.listdir(os.path.join(tmpdir,"clientoutgoing")):
            if file not in os.listdir(os.path.join(diskdir,"clientoutgoing")):
                shutil.copyfile(os.path.join(tmpdir,"clientoutgoing",file),os.path.join(diskdir,"clientoutgoing",file))
        for file in os.listdir(os.path.join(diskdir,"clientincoming")):
            if file not in os.listdir(os.path.join(tmpdir,"clientincoming")):
                shutil.copyfile(os.path.join(diskdir,"clientincoming",file),os.path.join(tmpdir,"clientincoming",file))

def savefile(data):
    disk = getdisk()
    tmpdir = os.path.join(tempfile.gettempdir(),"carnivaldata")
    filename = base64.urlsafe_b64encode(str(time.time()).encode()[-8:]+os.urandom(4)).decode()
    with open(os.path.join(tmpdir,"clientoutgoing",filename+".crn"),"w+") as savefile:
        savefile.write(data)
        savefile.close()
    syncdata()

@app.route('/')
def index():
    syncdata()
    return flask.render_template('index.html')
@app.route('/entertestrace',methods = ['POST'])
def entertestrace():
    data = flask.request.form['d']
    savefile(data)

if __name__ == "__main__":
    webbrowser.open("http://localhost:6829")
    app.run(port="6829",host="localhost")
