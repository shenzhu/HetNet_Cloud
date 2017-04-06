from flask import render_template,Response
from . import routes
from server import *
import json

@routes.route('/uploadapplication', methods=['POST'])
def upload_application_data():
    applicationDataJSON = request.get_json()

    # Extract data from post json
    name = applicationDataJSON['name']
    device_id = applicationDataJSON['device_id']

    # Check if foreign key exists
    loginCursor = g.conn.execute('SELECT * FROM login WHERE device_id = %s', device_id)
    loginRows = []
    for row in loginCursor:
        loginRows.append(row)

    # Insert into database
    if len(loginRows) > 0:
        applicationCursor = g.conn.execute('INSERT INTO application(name, device_id) VALUES(%s, %s)',
                                           name, device_id)
        responseJSON = {"status": "Success"}
    else:
        responseJSON = {"status": "Failure"}
        print "ERROR! No corresponding primary key"

    return Response(response=json.dumps(responseJSON), status=200, mimetype="application/json")

@routes.route('/uploadappdetl', methods=['POST'])
def upload_appdetl_data():
    appdetlDataJSON = request.get_json()

    # Extract data from post json
    access_time = appdetlDataJSON['access_time']
    type = appdetlDataJSON['type']
    name = appdetlDataJSON['name']
    interval = appdetlDataJSON['interval']
    value = appdetlDataJSON['value']
    device_id = appdetlDataJSON['device_id']

    # Check if name and device_id exists in application
    applicationCursor = g.conn.execute('SELECT * FROM application WHERE name=%s, device_id=%s', name, device_id)
    applicationRows = []
    for row in applicationCursor:
        applicationRows.append(row)

    # Insert into database
    if len(applicationRows) > 0:
        appdetlCursor = g.conn.execute(
            'INSERT INTO appdetl(access_time, type, name, interval, value, device_id) VALUES(%s, %s, %s, %s, %s, %s)',
            access_time, type, name, interval, value, device_id)
        responseJSON = {"status": "Success"}
    else:
        responseJSON = {"status": "Failure"}
        print "ERROR! No corresponding primary key"

    return Response(response=json.dumps(responseJSON), status=200, mimetype="application/json")
    

