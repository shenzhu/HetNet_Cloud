from flask import render_template,Response
from . import routes
from server import *
import json


@routes.route('/appdata', methods=['POST'])
def upload_application():
    application_data = request.get_json()

    # Extract data from post json
    applications = application_data["Applications"]
    device_id = application_data["device_id"]
    time = application_data["Time"]

    # Check if device_id in login table
    login_cursor_select = g.conn.execute('SELECT * FROM login WHERE device_id = %s',
                                         device_id)
    if login_cursor_select.rowcount == 0:
        g.conn.execute('INSERT INTO login(device_id, password, email) VALUES(%s, %s, %s)',
                       device_id, "password", "email")

    # Insert into database
    try:
        for application in applications:

            # Find if appliaction data already in database
            cursor_select = g.conn.execute('SELECT * FROM appdata WHERE uid = %s AND device_id = %s',
                                           application["uid"], device_id)
            if cursor_select.rowcount == 0:
                cursor_insert = g.conn.execute('INSERT INTO appdata(uid, timestamp, download, application_package, upload, device_id, time) VALUES(%s, %s, %s, %s, %s, %s, %s)',
                                               application["uid"], application["time"], application["download"],
                                               application["application_package"], application["upload"], device_id, time)
            else:
                pass

    except Exception as e:
        print e
        response_json = {"Status": "Failure"}
        return Response(response=json.dumps(response_json), status=400, mimetype="application/json")

    response_json = {"Status": "Success"}
    return Response(response=json.dumps(response_json), status=200, mimetype="application/json")


@routes.route('/getappdata', methods=['GET'])
def get_application():

    try:
        cursor_select = g.conn.execute('SELECT * FROM appdata')

        results = []
        for row in cursor_select:
            uid = row['uid']
            timestamp = row['timestamp']
            download = row['download']
            application_package = row['application_package']
            upload = row['upload']
            device_id = row['device_id']
            time = row['time']

            appdata = [int(uid), int(timestamp), float(download), application_package, float(upload), device_id, time]
            results.append(appdata)

        return Response(response=json.dumps(results), status=200, mimetype="application/json")

    except Exception as e:
        print e

        response_json = {"Status": "Failure"}
        return Response(response=json.dumps(response_json), status=500, mimetype="application/json")