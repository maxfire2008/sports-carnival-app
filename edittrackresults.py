print("Module EditTrackResults loaded.")
from app import app, savefile, openfile, loaddata, getuid
import flask
import json

@app.route("/edittrackresults/<eventid>")
def edittrackresults(eventid):
    data = loaddata()
    if "events" in data and eventid in data["events"] and data["events"][eventid] != None:
        return flask.render_template("edittrackresults.html",eventid=eventid)
    else:
        return "Event not found"

# @app.route("/api/savestudents/<eventid>",methods = ['POST'])
# def savestudents(eventid):
    # print(flask.request.data.decode())
    # requestdata = json.loads(flask.request.data.decode())
    # currentdata = loaddata()
    # newdata = currentdata["events"][eventid]["entrants"]
    # for student in requestdata:
        # if requestdata[student] != "" and student in newdata and newdata[student] != None and (int(requestdata[student])-1) != newdata[student]["heat"]:
            # newdata[student]["heat"] = int(requestdata[student])-1
        # elif requestdata[student] != "" and (student not in newdata or newdata[student] == None):
            # newdata[student] = {'type': 'time', 'time': None, 'heat': int(requestdata[student])-1}
        # elif student in newdata and newdata[student] != None and requestdata[student] == "":
            # print("needtoremove")
            # newdata[student] = None
    # print(newdata)
    # savefile(json.dumps({"events":{eventid:{"entrants":newdata}}}))
    # return ""