from flask import render_template,Response
from . import routes
from application import *
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


@routes.route('/network/getall', methods=['GET'])
def get_all_network():
    """
    get all network
    :return: {
        "networks": []
    }
    """

    try:
        cursor_select = g.conn.execute('SELECT * FROM networks');

        results = {}
        results["networks"] = []

        for row in cursor_select:
            network = {
                "ssid": row['ssid'],
                "bandwidth": int(row['bandwidth']),
                "location": row['location'],
                "security": row['security'],
                "avgss": int(row['avgss']),
                "device_id": row['device_id'],
                "time": row['time']
            }

            results["networks"].append(network)

        return Response(response=json.dumps(results), status=200, mimetype="application/json")

    except Exception as e:
        print e

        response_json = {"Status": "Failure"}
        return Response(response=json.dumps(response_json), status=500, mimetype="application/json")


@routes.route('/network/bydeviceid', methods=['GET'])
def get_network_by_device_id():
    """
    get network by device_id
    :return: {
        "networks": [],
        "device_id": device_id_param
    }
    """

    device_id_param = request.args.get('deviceid')

    try:
        cursor_select = g.conn.execute('SELECT * FROM networks WHERE device_id = %s',
                                       device_id_param)

        results = {}
        results["networks"] = []
        results["device_id"] = device_id_param

        for row in cursor_select:
            network = {
                "ssid": row['ssid'],
                "bandwidth": int(row['bandwidth']),
                "location": row['location'],
                "security": row['security'],
                "avgss": int(row['avgss']),
                "device_id": row['device_id'],
                "time": row['time']
            }

            results["networks"].append(network)

        return Response(response=json.dumps(results), status=200, mimetype="application/json")

    except Exception as e:
        print e

        response_json = {"Status": "Failure"}
        return Response(response=json.dumps(response_json), status=500, mimetype="application/json")


@routes.route('/network/byssid', methods=['GET'])
def get_network_by_ssid():
    """
    get network by ssid
    :return: {
        "networks": [],
        "ssid": ssid_param
    }
    """

    ssid_param = request.args.get('ssid')

    try:
        cursor_select = g.conn.execute('SELECT * FROM networks WHERE ssid = %s',
                                       ssid_param)

        results = {}
        results["networks"] = []
        results["ssid"] = ssid_param

        for row in cursor_select:
            network = {
                "ssid": row['ssid'],
                "bandwidth": int(row['bandwidth']),
                "location": row['location'],
                "security": row['security'],
                "avgss": int(row['avgss']),
                "device_id": row['device_id'],
                "time": row['time']
            }

            results["networks"].append(network)

        return Response(response=json.dumps(results), status=200, mimetype="application/json")

    except Exception as e:
        print e

        response_json = {"Status": "Failure"}
        return Response(response=json.dumps(response_json), status=500, mimetype="application/json")


@routes.route('/network/bylocation', methods=['GET'])
def get_network_by_location():
    """
    get network by location
    :return: {
        "networks": [],
        "location": location_param
    }
    """

    location_param = request.args.get('location')

    try:
        cursor_select = g.conn.execute('SELECT * FROM networks WHERE location = %s',
                                       location_param)

        results = {}
        results["networks"] = []
        results["location"] = location_param
        for row in cursor_select:
            network = {
                "ssid": row['ssid'],
                "bandwidth": int(row['bandwidth']),
                "location": row['location'],
                "security": row['security'],
                "avgss": int(row['avgss']),
                "device_id": row['device_id'],
                "time": row['time']
            }

            results["networks"].append(network)

        return Response(response=json.dumps(results), status=200, mimetype="application/json")

    except Exception as e:
        print e

        response_json = {"Status": "Failure"}
        return Response(response=json.dumps(response_json), status=500, mimetype="application/json")


@routes.route('/network/bandwidth/bylocation', methods=['GET'])
def get_avg_bandwidth_by_location():
    """
    get the average bandwidth by location
    :return: {
        "avg_bandwidth": number,
        "location": location_param
    }
    """
    location_param = request.args.get('location')

    try:

        cursor_select = g.conn.execute('SELECT * FROM networks WHERE location = %s',
                                       location_param)

        bandwidth_sum = 0.0
        for row in cursor_select:
            bandwidth_sum += int(row['bandwidth'])

        # Construct results
        results = {}
        results["avg_bandwidth"] = bandwidth_sum / cursor_select.rowcount
        results["location"] = location_param

        return Response(response=json.dumps(results), status=200, mimetype="application/json")

    except Exception as e:
        print e

        response_json = {"Status": "Failure"}
        return Response(response=json.dumps(response_json), status=500, mimetype="application/json")


@routes.route('/network/bandwidth/getallavg/ssid', methods=['GET'])
def get_all_avg_bandwidth_by_ssid():
    """
    get all average bandwidth by ssid
    :return: {
        ssid: avg_bandwidth,
        ...
    }
    """
    try:

        cursor_select = g.conn.execute('SELECT * FROM networks WHERE ssid = %s',
                                       ssid_param)

        bandwidth_sum = 0.0
        for row in cursor_select:
            bandwidth_sum += int(row['bandwidth'])

        # Construct results
        results = {}
        results["avg_bandwidth"] = bandwidth_sum / cursor_select.rowcount
        results["ssid"] = ssid_param

        return Response(response=json.dumps(results), status=200, mimetype="application/json")

    except Exception as e:
        print e

        response_json = {"Status": "Failure"}
        return Response(response=json.dumps(response_json), status=500, mimetype="application/json")




@routes.route('/network/avgss/bylocation', methods=['GET'])
def get_avg_signal_strength_by_location():
    """
    get the average bandwidth by location
    :return: {
        "avg_signal_strength": number,
        "location": location_param
    }
    """
    location_param = request.args.get('location')

    print location_param

    try:

        cursor_select = g.conn.execute('SELECT * FROM networks WHERE location = %s',
                                       location_param)

        avgss_sum = 0.0
        for row in cursor_select:
            avgss_sum += int(row['avgss'])

        # Construct results
        results = {}
        results["avg_signal_strength"] = avgss_sum / cursor_select.rowcount
        results["location"] = location_param

        return Response(response=json.dumps(results), status=200, mimetype="application/json")

    except Exception as e:
        print e

        response_json = {"Status": "Failure"}
        return Response(response=json.dumps(response_json), status=500, mimetype="application/json")


@routes.route('/network/avgss/byssid', methods=['GET'])
def get_avg_signal_strength_by_ssid():
    """
    get the average bandwidth by location
    :return: {
        "avg_signal_strength": number,
        "location": location_param
    }
    """
    ssid_param = request.args.get('ssid')

    try:

        cursor_select = g.conn.execute('SELECT * FROM networks WHERE ssid = %s',
                                       ssid_param)

        avgss_sum = 0.0
        for row in cursor_select:
            avgss_sum += int(row['avgss'])

        # Construct results
        results = {}
        results["avg_signal_strength"] = avgss_sum / cursor_select.rowcount
        results["ssid"] = ssid_param

        return Response(response=json.dumps(results), status=200, mimetype="application/json")

    except Exception as e:
        print e

        response_json = {"Status": "Failure"}
        return Response(response=json.dumps(response_json), status=500, mimetype="application/json")


@routes.route('/getlocations', methods=['GET'])
def get_all_locations():
    """
    get all locations
    :return: [
        location,
        ...
    ]
    """

    try:
        location_list = []

        cursor_select = g.conn.execute('SELECT DISTINCT location FROM networks')
        for row in cursor_select:
            location_list.append(row[0])

        return Response(response=json.dumps(location_list), status=200, mimetype="application/json")
    except Exception as e:
        print e

        response_json = {"Status": "Failure"}
        return Response(response=json.dumps(response_json), status=500, mimetype="application/json")
