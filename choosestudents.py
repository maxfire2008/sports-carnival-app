print("Module ChooseStudents loaded.")
from app import app, savefile, openfile, loaddata
import flask

@app.route("/choosestudents/<eventid>")
def choosestudents(eventid):
    data = loaddata()
    return flask.render_template("choosestudents.html",eventid=eventid)