import flask
import webbrowser
import psutil
import os
import requests
import time
import base64
import tempfile
import shutil
import json

app = flask.Flask(__name__)

webpageuid = int(time.time()*5000)
def getuid():
    global webpageuid
    webpageuid += 1
    return webpageuid

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
            shutil.copyfile(os.path.join(tmpdir,"clientoutgoing",file),os.path.join(diskdir,"clientoutgoing",file))
        for file in os.listdir(os.path.join(diskdir,"clientincoming")):
            shutil.copyfile(os.path.join(diskdir,"clientincoming",file),os.path.join(tmpdir,"clientincoming",file))

def savefile(data):
    tmpdir = os.path.join(tempfile.gettempdir(),"carnivaldata")
    filename = str(int(time.time()*1000))
    with open(os.path.join(tmpdir,"clientoutgoing",filename+".cao"),"w+") as savefile:
        savefile.write(data)
        savefile.close()
    syncdata()
    return os.path.join(tmpdir,"clientoutgoing",filename+".cao")
def openfile(name):
    try:
        syncdata()
        tmpdir = os.path.join(tempfile.gettempdir(),"carnivaldata")
        return open(os.path.join(tmpdir,"clientincoming",name+".cai"),"rb").read().decode()
    except:
        return None
def data_merge(a, b):
    """merges b into a and return merged result

    NOTE: tuples and arbitrary objects are not handled as it is totally ambiguous what should happen"""
    key = None
    # ## debug output
    # sys.stderr.write("DEBUG: %s to %s\n" %(b,a))
    try:
        if isinstance(a, list):
            # lists can be only appended
            if isinstance(b, list):
                # merge lists
                a.extend(b)
            else:
                # append to list
                a = b
        elif isinstance(a, dict):
            # dicts must be merged
            if isinstance(b, dict):
                for key in b:
                    if key in a:
                        a[key] = data_merge(a[key], b[key])
                    else:
                        a[key] = b[key]
            else:
                a = b
        else:
            a = b
    except TypeError as e:
        print(e)
    return a
def loaddata():
    syncdata()
    dataloaded = {}
    disk = getdisk()
    if disk:
        diskdir = os.path.join(disk.mountpoint,"carnivaldata")
    tmpdir = os.path.join(tempfile.gettempdir(),"carnivaldata")
    filesread = []
    for filename in sorted(os.listdir(os.path.join(tmpdir,"clientincoming"))):
        if filename.endswith(".cai"):
            try:
                filecontents = json.loads(open(os.path.join(tmpdir,"clientincoming",filename),"rb").read().decode())
            except Exception as e:
                print(e,os.path.join(tmpdir,"clientincoming",filename))
                filecontents = {}
            filesread.append([filename,filecontents])
    if disk:
        for filename in sorted(os.listdir(os.path.join(diskdir,"clientincoming"))):
            if filename.endswith(".cai"):
                try:
                    filecontents = json.loads(open(os.path.join(diskdir,"clientincoming",filename),"rb").read().decode())
                except Exception as e:
                    print(e,os.path.join(diskdir,"clientincoming",filename))
                    filecontents = {}
                filesread.append([filename,filecontents])
        for filename in sorted(os.listdir(os.path.join(diskdir,"clientoutgoing"))):
            if filename.endswith(".cao"):
                try:
                    filecontents = json.loads(open(os.path.join(diskdir,"clientoutgoing",filename),"rb").read().decode())
                except Exception as e:
                    print(e,os.path.join(diskdir,"clientoutgoing",filename))
                    filecontents = {}
                filesread.append([filename,filecontents])
    for filename in sorted(os.listdir(os.path.join(tmpdir,"clientoutgoing"))):
        if filename.endswith(".cao"):
            try:
                filecontents = json.loads(open(os.path.join(tmpdir,"clientoutgoing",filename),"rb").read().decode())
            except Exception as e:
                print(e,os.path.join(tmpdir,"clientoutgoing",filename))
                filecontents = {}
            filesread.append([filename,filecontents])
    
    for file in sorted(filesread):
        # dataloaded = {**dataloaded,**file[1]}
        dataloaded = data_merge(dataloaded, file[1])
    
    return dataloaded

@app.route('/')
def index():
    syncdata()
    return flask.render_template('index.html')
@app.route('/api/recievedata',methods = ['POST'])
def recievedata():
    data = {"raw_data_at"+str(time.time()):{"rawrequest":flask.request.form['d'],"time":time.time()}}
    datajs = json.dumps(data)
    return savefile(datajs)
@app.route('/api/retrievedata')
def retrievedata():
    return json.dumps(loaddata())


import eventselect
import choosestudents
import edittrackresults

# if __name__ == "__main__":
    # webbrowser.open("http://localhost:6829")
    # app.run(port="6829",host="localhost")
