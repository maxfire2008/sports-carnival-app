print("Module ChooseStudents loaded.")
from app import app, savefile, openfile, loaddata, getuid
import flask
import json

@app.route("/choosestudents/<eventid>")
def choosestudents(eventid):
    data = loaddata()
    if "events" in data and eventid in data["events"] and data["events"][eventid] != None:
        for agegroup in data["students"]:
            for student in data["students"][agegroup]["students"]:
                if data["students"][agegroup]["students"][student]["prefname"]:
                    student_name = data["students"][agegroup]["students"][student]["prefname"]
                else:
                    student_name = data["students"][agegroup]["students"][student]["firstname"]+" "+data["students"][agegroup]["students"][student]["lastname"]
                # student_name = data["students"][agegroup]["students"][student]["firstname"]+" "+data["students"][agegroup]["students"][student]["lastname"]
                if student in data["events"][eventid]["entrants"]:
                    students.append([student_name,student,int(data["events"][eventid]["entrants"]["heat"])+1,getuid()])
                else:
                    students.append([student_name,student,"",getuid()])
        return flask.render_template("choosestudents.html",eventid=eventid,students=sorted(students))
    else:
        return "Event not found"

# @app.route("/savestudents/<eventid>",methods = ['POST'])
# def savestudents(eventid):
    # print(flask.request.data.decode())
    # requestdata = json.loads(flask.request.data.decode())
    # currentdata = loaddata()
    # newdata = currentdata[eventid]["heats"]
    # for student in requestdata:
        # if requestdata["student"] != "":
            # None
    # return ""