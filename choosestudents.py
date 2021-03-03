print("Module ChooseStudents loaded.")
from app import app, savefile, openfile, loaddata, getuid
import flask

@app.route("/choosestudents/<eventid>")
def choosestudents(eventid):
    data = loaddata()
    if "events" in data and eventid in data["events"]:
        studentsheats = {}
        allstudentsselected = []
        for heat in data["events"][eventid]["heats"]:
            inheat = []
            for student in data["events"][eventid]["heats"][heat]:
                inheat.append(student)
            studentsheats[heat] = inheat
            allstudentsselected+=inheat
        students = []
        for agegroup in data["students"]:
            if (data["events"][eventid]["gender"] == "*" or data["events"][eventid]["gender"] == data["students"][agegroup]["gender"]) and (data["events"][eventid]["year"] == "*" or data["events"][eventid]["year"] == data["students"][agegroup]["year"]):
                for student in data["students"][agegroup]["students"]:
                    if data["students"][agegroup]["students"][student]["prefname"]:
                        student_name = data["students"][agegroup]["students"][student]["prefname"]
                    else:
                        student_name = data["students"][agegroup]["students"][student]["firstname"]+" "+data["students"][agegroup]["students"][student]["lastname"]
                    if student in allstudentsselected:
                        for heatname in studentsheats:
                            if student in studentsheats[heatname]:
                                break
                        students.append([student_name,student,heatname,getuid()])
                    else:
                        students.append([student_name,student,"",getuid()])
        return flask.render_template("choosestudents.html",eventid=eventid,students=sorted(students))
    else:
        return "Event not found"