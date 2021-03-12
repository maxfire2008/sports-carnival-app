print("Module EditTrackResults loaded.")
from app import app, savefile, openfile, loaddata, getuid
import flask
import json

def intomsms(t):
    m=int(t/60000)
    s=int((t-(m*60000))/1000)
    ms=(t-(m*60000)-(s*1000))
    return m,s,ms

@app.route("/edittrackresults/<eventid>")
def edittrackresults(eventid):
    data = loaddata()
    if "events" in data and eventid in data["events"] and data["events"][eventid] != None:
        heats = {}
        for entrant in data["events"][eventid]["entrants"]:
            if data["events"][eventid]["entrants"][entrant] != None:
                if data["events"][eventid]["entrants"][entrant]["heat"] not in heats:
                    heats[data["events"][eventid]["entrants"][entrant]["heat"]] = []
                timeminutes = ""
                timeseconds = ""
                timemilliseconds = ""
                rank = ""
                if data["events"][eventid]["entrants"][entrant]["type"] == "time":
                    timeminutes,timeseconds,timemilliseconds = intomsms(data["events"][eventid]["entrants"][entrant]["time"])
                    timeminutes=str(timeminutes)
                    timeseconds=str(timeseconds)
                    timemilliseconds=str(timemilliseconds)
                if data["events"][eventid]["entrants"][entrant]["type"] == "rank":
                    rank = data["events"][eventid]["entrants"][entrant]["rank"]
                timestring = timeminutes+":"+timeseconds+":"+timemilliseconds
                if entrant in data["events"][eventid]["entrants"] and data["events"][eventid]["entrants"][entrant] != None and "display" in data["events"][eventid]["entrants"][entrant]:
                    studentdisplaylocation = int(data["events"][eventid]["entrants"][entrant]["display"])
                else:
                    studentdisplaylocation = 10000000
                for agegroup in data["students"]:
                    for student in data["students"][agegroup]["students"]:
                        if student == entrant:
                            if data["students"][agegroup]["students"][entrant]["prefname"]:
                                student_name = data["students"][agegroup]["students"][entrant]["prefname"]
                            else:
                                student_name = data["students"][agegroup]["students"][entrant]["firstname"]+" "+data["students"][agegroup]["students"][student]["lastname"]
                heats[data["events"][eventid]["entrants"][entrant]["heat"]].append([studentdisplaylocation,entrant,student_name,timestring,rank])
        return flask.render_template("edittrackresults.html",eventid=eventid,eventname=data["events"][eventid]["name"])
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