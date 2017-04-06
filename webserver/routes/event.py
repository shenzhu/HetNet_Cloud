from flask import render_template, Response
from . import routes
from server import *
import json
from flask import request


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


@routes.route('/uploadlogin', methods=['POST'])
def upload_login_data():
    loginDataJSON = request.get_json()

    # Extract data from post json
    device_id = loginDataJSON['device_id']
    password = loginDataJSON['password']
    email = loginDataJSON['email']

    # Insert into database
    cursor = g.conn.execute('INSERT INTO login(device_id, password, email) VALUES(%s, %s, %s)', device_id, password,
                            email)
    responseJSON = {"status": "Success"}

    return Response(response=json.dumps(responseJSON), status=200, mimetype="application/json")


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


@routes.route('/register', methods=['POST'])
def register_new_user():
    userDataJSON = request.get_json()

    # Extract name, email and password
    name = userDataJSON['name']
    password = userDataJSON['password']
    email = userDataJSON['email']

    print "EXECUTED"

    # Check if email already exists
    cursor = g.conn.execute('SELECT * FROM login WHERE email=%s', email)
    results = []
    for row in cursor:
        results.append(row)

    print results

    device_id = 4
    # Insert into database
    if len(results) == 0:
        g.conn.execute('INSERT INTO login(device_id, password, email) VALUES(%s, %s, %s)',
                       device_id, password, email)
        responseJSON = {"status": "Success"}
    else:
        responseJSON = {"status": "Failure"}
        print "ERROR!"

    return Response(response=json.dumps(responseJSON), status=200, mimetype="application/json")


def table_name_extracter(name):
    cursor = g.conn.execute('SELECT column_name FROM information_schema.columns WHERE table_name= %s', name)
    names = []
    for row in cursor:
        names.append(row[0])
    return names


@routes.route('/coach')
def coach():
    return render_template("coach.html")


@routes.route('/coach/gethalls', methods=['GET'])
def halls():
    halls_data = []
    cursor = g.conn.execute('SELECT * from hall;')
    for row in cursor:
        temp = {'location': '', 'name': '', 'capacity': ''}
        temp['location'] = row[0]
        temp['name'] = row[1]
        temp['capacity'] = row[2]
        halls_data.append(temp)
    resp = Response(response=json.dumps(halls_data), status=200, mimetype="application/json")
    return (resp)


@routes.route('/coach/getavailablehall', methods=['POST'])
def available_hall():
    data = request.get_json()
    availability = []
    cursor = g.conn.execute('SELECT timeslot from instruction where name = %s', data['name'])
    for row in cursor:
        availability.append(row[0])
    resp = Response(response=json.dumps(availability), status=200, mimetype="application/json")
    return (resp)


@routes.route('/coach/gettrain', methods=['POST'])
def trainning():
    data = request.get_json()
    trainning_data = []
    cursor = g.conn.execute(
        'select time, date, coaid, name from train inner join member on (train.pid = member.pid) where coaid = %s;',
        data['coaid'])
    for row in cursor:
        temp = {'time': '', 'date': '', 'coaid': '', 'Member': ''}
        temp['time'] = row[0].strftime('%H:%M:%S')
        temp['date'] = row[1].strftime('%Y-%m-%d')
        temp['coaid'] = row[2]
        temp['Member'] = row[3]
        trainning_data.append(temp)
    resp = Response(response=json.dumps(trainning_data), status=200, mimetype="application/json")
    return (resp)


def checkcid(cid):
    cursor = g.conn.execute('SELECT cid from course where cid = %s', cid)
    existed = False
    for row in cursor:
        existed = True
    return existed


@routes.route('/coach/addinstruction', methods=['POST'])
def addinstruction():
    data = request.get_json()
    if not check_time_hall(data['week'], data['time'], data['hall']):
        cursor = g.conn.execute('INSERT INTO instruction VALUES(%s,%s,%s,%s,%s)', data['coaid'], data['course'],
                                data['hall'], data['week'], data['time'])
        resp = Response(response=json.dumps([{'result': 'Success'}]), status=200, mimetype="application/json")
    else:
        resp = Response(response=json.dumps([{'result': 'Failed'}]), status=200, mimetype="application/json")
    return (resp)


def check_time_hall(week, time, hall):
    cursor = g.conn.execute('SELECT * from instruction where week = %s and time = %s and hallname = %s', week, time,
                            hall)
    existed = False
    for row in cursor:
        existed = True
    return existed


@routes.route('/coach/getinstruction', methods=['POST'])
def getinstruction():
    data = request.get_json()
    result = []
    table_names = table_name_extracter('instruction')
    cursor = g.conn.execute('SELECT * from instruction where coaid = %s', data['coaid'])
    for row in cursor:
        temp = {}
        for i in range(len(table_names)):
            temp[table_names[i]] = row[i]
        result.append(temp)
    resp = Response(response=json.dumps(result), status=200, mimetype="application/json")
    return (resp)


@routes.route('/coach/insmat', methods=['GET'])
def getcourse():
    cursor = g.conn.execute('SELECT cid,name from course;')
    data1 = []
    for row in cursor:
        data1.append(row[0] + ':' + row[1])
    data1 = {'course': data1}
    cursor = g.conn.execute('SELECT name from hall;')
    data2 = []
    for row in cursor:
        data2.append(row[0])
    data2 = {'hall': data2}
    data3 = {'week': range(1, 8)}
    data4 = {'time': range(19, 23)}
    resp = Response(response=json.dumps([data1, data2, data3, data4]), status=200, mimetype="application/json")
    return (resp)


@routes.route('/coach/delinstruction', methods=['DELETE'])
def delinstruction():
    data = request.get_json()
    cursor = g.conn.execute('delete from instruction where coaid = %s and time = %s and week = %s', data['coaid'],
                            data['time'], data['week'])
    resp = Response(response=json.dumps([{"result": "success"}]), status=200, mimetype="application/json")
    return (resp)
