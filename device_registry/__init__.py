import markdown
import os
import shelve

#import the flask framework
from flask import Flask, g, request, jsonify


#Create an instance of flask
app = Flask(__name__)
app.config["DEBUG"] = True

# Test books library
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]


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


@app.route('/', methods=['GET'])
def index():
    """Present some documentation"""
    #Open the readme file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r',  encoding='utf-8') as markdown_file:

        #Read the content of the file
        content = markdown_file.read()

        #Convert to HTML
        return markdown.markdown(content)

#Test api for books library
@app.route('/books', methods=['GET'])
def api_books():
    #return jsonify(books)
    #return {'message': 'Success', 'data': books}
    return jsonify({'message': 'Success', 'data': books})


@app.route('/devices/all', methods=['GET']) 
def api_all():
    shelf = get_db()
    keys = list(shelf.keys())

    devices = []

    for key in keys:
        devices.append(shelf[key])

    return {'message': 'Success', 'data': devices}, 200

@app.route('/devices', methods=['GET']) 
def api_getDevice():

    # If no ID is provided, display an error in the browser
    if 'identifier' in request.args:
        identifier = request.args['identifier']
        response = {'message': 'Get device by identifier', 'identifier': identifier}
        shelf = get_db()
        if not (identifier in shelf):
            response['result'] = 'Device not found'
            return response, 404
        else:
            response['result'] = shelf[identifier]
            return response, 200
    else:
        response = {'message': 'Error: No identifier field provided. Please specify an identifier.'}
        return response, 404

    #this does not include the response code
    #return response

@app.route('/device', methods=['DELETE'])
def api_deleteDevice():
    # If no ID is provided, display an error in the browser
    if 'identifier' in request.args:
        identifier = request.args['identifier']
        response = {'message': 'Remove device by identifier', 'identifier': identifier}
        shelf = get_db()
        if not (identifier in shelf):
            response['result'] = 'Device not found'
            return response, 404
        else:
            del shelf[identifier]
            response['result'] = 'Success'
			#you can use 204, but no content will be returned.  I would like a response
            return response, 200
    else:
        response = {'message': 'Error: No identifier field provided. Please specify an identifier.'}
        return response, 404

    #this does not include the response code
    #return response


@app.route('/device', methods=['POST']) 
def api_addupdDevice():
    validPayload = 1
    identifier = ''
    name = ''
    device_type = ''
    controller_gateway = ''
    response = ''
    processed = ''

    if 'identifier' in request.args:
        identifier = request.args['identifier']
        validPayload = 1

    if 'name' in request.args:
        name = request.args['name']

    if 'device_type' in request.args:
        device_type = request.args['device_type']

    if 'controller_gateway' in request.args:
        controller_gateway = request.args['controller_gateway']

    if validPayload == 1:
        processed = {'identifier': identifier }
        processed['name'] = name
        processed['device_type'] = device_type
        processed['controller_gateway'] = controller_gateway
        shelf = get_db()
        shelf[processed['identifier']] = processed
        response = {'message': 'Device Created or Updated'}
        response['payload'] = request.args
        response['processed'] = processed
        return response, 201

    else:
        response = {'message': 'Error: No identifier field provided. Please specify an identifier.'}
        response['payload'] = request.args
        return response, 404



@app.route('/deviceTest', methods=['POST']) 
def api_testDevice():
    validPayload = 1
    identifier = ''
    name = ''
    device_type = ''
    controller_gateway = ''
    response = ''
    if 'identifier' in request.args:
        identifier = request.args['identifier']
        validPayload = 1
    response = {'message': 'Test Response.', 'payload': request.args}
    return response, 200