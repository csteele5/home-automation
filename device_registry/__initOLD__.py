import markdown
import os
import shelve

#import the flask framework
from flask import Flask, g

from flask_restful import Resource

#Create an instance of flask
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("devices.db")
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def index():
	"""Present some documentation"""
	#Open the readme file
	with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

		#Read the content of the file
		content = markdown_file.read()

		#Convert to HTML
		return markdown.markdown(content)

class DeviceList(Resource):
	def get(self):
		shelf = get_db()
		keys = list(shelf.keys())

		devices = []

		for key in keys:
			devices.append(shelf[key])

		return {'message': 'Success', 'data': devices}

api.add_resource(DeviceList, '/devices')
