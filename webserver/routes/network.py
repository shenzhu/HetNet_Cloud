from flask import render_template,Response
from . import routes
from server import *
import json

@routes.route('/uploadnetwork', methods=['POST'])
def upload_network_data():
    networkDataJSON = request.get_json()

    # Extract data from post json
    ssid = networkDataJSON['ssid']
    bandwidth = networkDataJSON['bandwidth']
    security = networkDataJSON['security']
    location = networkDataJSON['location']
    avgss = networkDataJSON['avgss']
    device_id = networkDataJSON['device_id']

    # Check login table if device_id exists
    loginCursor = g.conn.execute('SELECT * FROM login WHERE device_id = %s', device_id)
    loginRows = []
    for row in loginCursor:
        loginRows.append(row)

    if len(loginRows) > 0:
        # Insert to database
        networkCursor = g.conn.execute(
            'INSERT INTO networks(ssid, bandwidth, security, location, avgss, device_id) VALUES(%s, %s, %s, %s, %s, %s)',
            ssid, bandwidth, security, location, avgss, device_id)
        responseJSON = {"status": "Success"}
    else:
        responseJSON = {"status": "Failure"}
        print "ERROR! No corresponding primary key"

    return Response(response=json.dumps(responseJSON), status=200, mimetype="application/json")
