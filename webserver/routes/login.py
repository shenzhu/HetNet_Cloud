from flask import render_template,Response, jsonify
from . import routes
from server import *
import json

@routes.route('/another')
def another():
    return render_template("login_template.html")


@routes.route('/login', methods=['POST'])
def login():
    loginDataJSON = request.get_json()

    # Extract data from post JSON
    email = loginDataJSON['Email']
    password = loginDataJSON['Password']

    # Check database
    cursor = g.conn.execute('SELECT * FROM login WHERE email = %s AND password = %s', email, password)
    resultRows = []
    for row in cursor:
        resultRows.append(row)

    if len(resultRows) > 0:
        responseJSON = {"status": "Success"}
    else:
        responseJSON = {"status": "Failure"}

    return Response(response=json.dumps(responseJSON), status=200, mimetype="application/json")

"""
@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    returned = {'id':'', 'identity':''}
    #print type(data) data type dict
    #  yg5632 Yu Gu
    cursor = g.conn.execute('SELECT pid from member where pid = %s and name = %s;', data['name'],data['password'])
    for row in cursor:
        returned['id'] = row[0]
        returned['identity'] = 'member'
    cursor = g.conn.execute('SELECT coaid from coach where coaid = %s and name = %s;', data['name'],data['password'])
    for row in cursor:
        returned['id'] = row[0]
        returned['identity'] = 'coach'
    cursor = g.conn.execute('SELECT manid from manager where manid = %s and name = %s;', data['name'],data['password'])
    for row in cursor:
        returned['id'] = row[0]
        returned['identity'] = 'manager'
    passed_data = [returned]
    json_data = json.dumps(passed_data)
    resp = Response(response=json_data,status=200, mimetype="application/json")
    return(resp)
"""
