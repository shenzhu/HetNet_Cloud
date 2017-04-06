from flask import render_template,Response
from . import routes
from server import *
import json


@routes.route('/network', methods=['POST'])
def upload_network():
    network_data = request.get_json()

    # Extract data from json
    networks = network_data["Networks"]

    location = network_data["location"].split(",")
    location = str(location[0][:8]) + ',' + str(location[1][:7])

    device_id = network_data["device_id"]
    time = network_data["Time"]

    # Check if device_id exists in login table
    login_cursor_select = g.conn.execute('SELECT * FROM login WHERE device_id = %s',
                                         device_id)
    if login_cursor_select.rowcount == 0:
        g.conn.execute('INSERT INTO login(device_id, password, email) VALUES(%s, %s, %s)',
                       device_id, "password", "test@columbia.edu")

    # Insert into database
    try:
        for network in networks:
            if int(network["bandwidth"]) == 0:
                continue

            # Find if network already exists in database
            cursor_select = g.conn.execute('SELECT * FROM networks WHERE ssid = %s AND location = %s',
                                    network["ssid"], location)
            if cursor_select.rowcount == 0:
                cursor_insert = g.conn.execute('INSERT INTO networks(ssid, bandwidth, security, location, avgss, device_id, time) VALUES(%s, %s, %s, %s, %s, %s, %s)',
                                               network["ssid"], network["bandwidth"], network["security"],
                                               location, network["avgss"], device_id, time)
            else:
                pass
    except Exception as e:
        print e

        response_json = {"Status": "Failure"}
        return Response(response=json.dumps(response_json), status=400, mimetype="application/json")

    response_json = {"Status": "Success"}
    return Response(response=json.dumps(response_json), status=200, mimetype="application/json")

