import flask
import csv
import json

data = {}

with open("../requests/itemData.csv", mode="r") as file:
    reader = csv.reader(file)
    with open("../requests/itemData.csv", mode="w") as outfile:
        writer = csv.writer(outfile)
        data = {rows[0]:rows[1] for rows in reader}
        print(data)

print(data)



app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

app.run()