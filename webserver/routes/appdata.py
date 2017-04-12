from flask import render_template,Response
from . import routes
from application import *
import json


@routes.route('/appdata', methods=['POST'])
def upload_application():
    """
    upload appdata to database
    :return: {"Status": "Success"} /
             {"Status": "Failure"}
    """

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
            cursor_select = g.conn.execute('SELECT * FROM appdata WHERE uid = %s AND device_id = %s AND time = %s',
                                           application["uid"], device_id, time)
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


@routes.route('/appdata/getall', methods=['GET'])
def get_all_app_data():
    """
    get all appdata
    :return: {
        "appdata": []
    }
    """

    try:
        cursor_select = g.conn.execute('SELECT * FROM appdata')

        results = {}
        results['appdata'] = []
        for row in cursor_select:
            uid = row['uid']
            timestamp = row['timestamp']
            download = row['download']
            application_package = row['application_package']
            upload = row['upload']
            device_id = row['device_id']
            time = row['time']

            appdata = {
                "uid": int(uid),
                "timestamp": float(timestamp),
                "download": float(download),
                "application_package": application_package,
                "upload": float(upload),
                "device_id": device_id,
                "time": time
            }
            results['appdata'].append(appdata)

        return Response(response=json.dumps(results), status=200, mimetype="application/json")

    except Exception as e:
        print e

        response_json = {"Status": "Failure"}
        return Response(response=json.dumps(response_json), status=500, mimetype="application/json")


@routes.route('/appdata/bydeviceid', methods=['GET'])
def get_appdata_by_device_id():
    """
    get appdata by device_id
    :return: {
        "appdata": [],
        "device_id": device_id_param
    }
    """

    device_id_param = request.args.get('deviceid')

    try:
        cursor_select = g.conn.execute('SELECT * FROM appdata WHERE device_id = %s',
                                       device_id_param)

        results = {}
        results["appdata"] = []
        results["device_id"] = device_id_param

        for row in cursor_select:
            uid = row['uid']
            timestamp = row['timestamp']
            download = row['download']
            application_package = row['application_package']
            upload = row['upload']
            device_id = row['device_id']
            time = row['time']

            appdata = {
                "uid": int(uid),
                "timestamp": float(timestamp),
                "download": float(download),
                "application_package": application_package,
                "upload": float(upload),
                "device_id": device_id,
                "time": time
            }
            results['appdata'].append(appdata)

        return Response(response=json.dumps(results), status=200, mimetype="application/json")


    except Exception as e:
        print e

        response_json = {"Status": "Failure"}
        return Response(response=json.dumps(response_json), status=500, mimetype="application/json")


@routes.route('/appdata/byuid', methods=['GET'])
def get_appdata_by_uid():
    """
    get appdata by uid
    :return: {
        "appdata": [],
        "uid": uid_param
    }
    """

    uid_param = request.args.get('uid')

    try:
        cursor_select = g.conn.execute('SELECT * FROM appdata WHERE uid = %s',
                                       uid_param)

        results = {}
        results["appdata"] = []
        results["uid"] = uid_param

        for row in cursor_select:
            uid = row['uid']
            timestamp = row['timestamp']
            download = row['download']
            application_package = row['application_package']
            upload = row['upload']
            device_id = row['device_id']
            time = row['time']

            appdata = {
                "uid": int(uid),
                "timestamp": float(timestamp),
                "download": float(download),
                "application_package": application_package,
                "upload": float(upload),
                "device_id": device_id,
                "time": time
            }
            results['appdata'].append(appdata)

        return Response(response=json.dumps(results), status=200, mimetype="application/json")


    except Exception as e:
        print e

        response_json = {"Status": "Failure"}
        return Response(response=json.dumps(response_json), status=500, mimetype="application/json")


@routes.route('/appdata/getbyapplicationpackage', methods=['GET'])
def get_appdata_by_application_package():
    """
    get appdata by application_package
    :return: {
        "appdata": [],
        "application_package": application_package_param
    }
    """

    application_package_param = request.args.get('applicationpackage')

    try:
        cursor_select = g.conn.execute('SELECT * FROM appdata WHERE application_package = %s',
                                       application_package_param)

        results = {}
        results["appdata"] = []
        results["application_package"] = application_package_param

        for row in cursor_select:
            uid = row['uid']
            timestamp = row['timestamp']
            download = row['download']
            application_package = row['application_package']
            upload = row['upload']
            device_id = row['device_id']
            time = row['time']

            appdata = {
                "uid": int(uid),
                "timestamp": float(timestamp),
                "download": float(download),
                "application_package": application_package,
                "upload": float(upload),
                "device_id": device_id,
                "time": time
            }
            results['appdata'].append(appdata)

        return Response(response=json.dumps(results), status=200, mimetype="application/json")


    except Exception as e:
        print e

        response_json = {"Status": "Failure"}
        return Response(response=json.dumps(response_json), status=500, mimetype="application/json")


@routes.route('/appdata/downloadstats', methods=['GET'])
def get_download_stats():
    """
    get download percentage of different applications
    :return: {
        app: percentage,
        ...
    }
    """

    try:
        cursor_select = g.conn.execute('SELECT * FROM appdata;')

        download_stats = {}
        download_sum = 0.0

        # Calculate stats of download by application_package
        for row in cursor_select:

            download = float(row['download'])
            application_package = row['application_package']

            if application_package not in download_stats:
                download_stats[application_package] = 0.0
            download_stats[application_package] = download + download_stats[application_package]
            download_sum = download + download_sum


        # Calculate download percentage by application_package
        for key in download_stats:
            download_stats[key] = (download_stats[key] / download_sum)


        return Response(response=json.dumps(download_stats), status=200, mimetype="application/json")


    except Exception as e:
        print e

        response_json = {"Status": "Failure"}
        return Response(response=json.dumps(response_json), status=500, mimetype="application/json")


@routes.route('/appdata/uploadstats', methods=['GET'])
def get_upload_stats():
    """
    get upload data percentage of different applications
    :return: {
        app: percentage,
        ...
    }
    """

    try:
        cursor_select = g.conn.execute('SELECT * FROM appdata;')

        upload_stats = {}
        upload_sum = 0.0

        # Calculate stats of download by application_package
        for row in cursor_select:

            upload = float(row['upload'])
            application_package = row['application_package']

            if application_package not in upload_stats:
                upload_stats[application_package] = 0.0
                upload_stats[application_package] = upload + upload_stats[application_package]
                upload_sum = upload + upload_sum


        # Calculate download percentage by application_package
        for key in upload_stats:
            upload_stats[key] = (upload_stats[key] / upload_sum)


        return Response(response=json.dumps(upload_stats), status=200, mimetype="application/json")


    except Exception as e:
        print e

        response_json = {"Status": "Failure"}
        return Response(response=json.dumps(response_json), status=500, mimetype="application/json")