print("Module EventSelect loaded.")
from app import app, savefile, openfile
import flask

@app.route("/eventselect")
def eventselect():
    return flask.render_template("eventselect.html",students=)
