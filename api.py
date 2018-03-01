from flask import Flask, render_template, request, redirect
from flask import jsonify
from wtforms import Form,StringField, IntegerField,HiddenField
from datetime import datetime, timedelta
from requests import get
import json

app = Flask(__name__)
usersJsonFile = 'test.json'

@app.route('/')
def index():
    with open(usersJsonFile , 'r') as jsonFile:
        users = json.load(jsonFile)
        return render_template('index.html',users=users)


@app.route('/getallusers')
def getallusers():
    with open(userJsonFile , 'r') as jsonFile:
        data = json.load(jsonFile)
        return jsonify(data)


@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    form = UserForm(request.form)
    if(request.method == 'POST'):
        with open(usersJsonFile, 'r+') as jsonFile:
            users = json.load(jsonFile)
            numberOfUsers = len(users)
            id = numberOfUsers + 1
            user = form.user.data
            port = users[numberOfUsers-1]['port'] + 1
            password = 'Pass@word' + str(port)
            expire = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            users.append(
                {
                    "d": 0,
                    "enable": 1,
                    "forbidden_port": "",
                    "method": "aes-128-ctr",
                    "obfs": "tls1.2_ticket_auth_compatible",
                    "passwd": password,
                    "port": port,
                    "protocol": "auth_aes128_md5",
                    "protocol_param": "3",
                    "speed_limit_per_con": 0,
                    "speed_limit_per_user": 0,
                    "transfer_enable": 900727656415232,
                    "u": 0,
                    "user": user,
                    "expire": expire,
                    "id": id
                }
            )
            jsonFile.seek(0)  # rewind
            json.dump(users, jsonFile)
            jsonFile.truncate()
            return redirect('/') 

    return render_template('adduser.html', form=form)


@app.route('/updateuser/<int:id>/', methods=['GET', 'POST'])
def updateuser(id):
    form = UserForm(request.form)
    if(request.method == 'POST'):

        user = form.user.data
        port = form.port.data
        password = form.password.data
        with open(usersJsonFile, 'r+') as jsonFile:
            users = json.load(jsonFile)
            updateUser = users[id-1]
            updateUser['user'] = user
            updateUser['passwd'] = password
            jsonFile.seek(0)  # rewind
            json.dump(users, jsonFile)
            jsonFile.truncate()
            return redirect('/')
    else:
        with open(usersJsonFile, 'r+') as jsonFile:
            users = json.load(jsonFile)
            user = users[id-1]
            form.id.data = user['id']
            form.user.data = user['user']
            form.password.data = user['passwd']
            form.port.data = user['port']
            form.deviceLimited.data = user['protocol_param']
            form.expire.data = user['expire']
            # print(user)
            return render_template('updateuser.html', form=form)


@app.route('/connectioninfo/<int:id>')
def getconnectioninfo(id):
    ip = get('https://api.ipify.org').text
    with open(usersJsonFile, 'r+') as jsonFile:
        users = json.load(jsonFile)
        user = users[id-1]
        user['ip'] = ip
        return render_template('connectioninfo.html' , user=user)

class UserForm(Form):
    #read only
    id = IntegerField('Id', render_kw={'readonly': True})
    port = IntegerField('Port' , render_kw={'readonly': True})
    deviceLimited = StringField('DeviceLimited', render_kw={'readonly': True})
    # editable
    user = StringField('User')
    password = StringField('Password')
    expire = StringField('Expire')

if __name__ == '__main__':
    app.run(debug=True)