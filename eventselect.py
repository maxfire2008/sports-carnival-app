print("Module EventSelect loaded.")
from app import app, savefile, openfile, loaddata
import flask

@app.route("/eventselect")
def eventselect():
    data = loaddata()
    events = []
    if "events" in data:
        try:
            for event in data["events"]:
                try:
                    events.append([event,data["events"][event]["name"],data["events"][event]["type"]])
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
    return flask.render_template("eventselect.html",events=events)