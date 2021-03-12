print("Module ChooseStudents loaded.")
from app import app, savefile, openfile, loaddata, getuid
import flask
import json

@app.route("/choosestudents/<eventid>")
def choosestudents(eventid):
    data = loaddata()
    if "events" in data and eventid in data["events"] and data["events"][eventid] != None:
        students = []
        for agegroup in data["students"]:
            if data["students"][agegroup] != None and (data["events"][eventid]["gender"] == data["students"][agegroup]["gender"] or data["events"][eventid]["gender"] == "*") and (data["events"][eventid]["year"] == data["students"][agegroup]["year"] or data["events"][eventid]["year"] == "*"):
                for student in data["students"][agegroup]["students"]:
                    if data["students"][agegroup]["students"][student]["prefname"]:
                        student_name = data["students"][agegroup]["students"][student]["prefname"]
                    else:
                        student_name = data["students"][agegroup]["students"][student]["firstname"]+" "+data["students"][agegroup]["students"][student]["lastname"]
                    # student_name = data["students"][agegroup]["students"][student]["firstname"]+" "+data["students"][agegroup]["students"][student]["lastname"]
                    if student in data["events"][eventid]["entrants"] and data["events"][eventid]["entrants"][student] != None:
                        students.append([int(data["events"][eventid]["entrants"][student]["display"]),student_name,student,int(data["events"][eventid]["entrants"][student]["heat"])+1,getuid()])
                    else:
                        students.append([10000000,student_name,student,"",getuid()])
        return flask.render_template("choosestudents.html",eventid=eventid,students=sorted(students),eventname=data["events"][eventid]["name"])
    else:
        return "Event not found"

@app.route("/api/savestudents/<eventid>",methods = ['POST'])
def savestudents(eventid):
    print(flask.request.data.decode())
    requestdata = json.loads(flask.request.data.decode())
    currentdata = loaddata()
    newdata = currentdata["events"][eventid]["entrants"]
    for student in requestdata:
        if requestdata[student] != "" and student in newdata and newdata[student] != None and (int(requestdata[student])-1) != newdata[student]["heat"]:
            newdata[student]["heat"] = int(requestdata[student])-1
        elif requestdata[student] != "" and (student not in newdata or newdata[student] == None):
            newdata[student] = {'type': 'time', 'time': None, 'heat': int(requestdata[student])-1}
        elif student in newdata and newdata[student] != None and requestdata[student] == "":
            print("needtoremove")
            newdata[student] = None
    print(newdata)
    savefile(json.dumps({"events":{eventid:{"entrants":newdata}}}))
    return ""