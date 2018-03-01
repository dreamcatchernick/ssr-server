from flask import Flask, render_template, request, redirect
from flask import jsonify
from wtforms import Form,StringField, IntegerField,HiddenField
from datetime import datetime, timedelta
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
        with open(usersJsonFile, 'r+') as jsonFile:
            users = json.load(jsonFile)
            return str(len(users))

@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    form = UserForm(request.form)
    if(request.method == 'POST'):
        user = form.user.data
        password = 'Pass@word1'
        expire = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        # print(user.data)

        with open(usersJsonFile, 'r+') as jsonFile:
            users = json.load(jsonFile)
            id = len(users) + 1
            users.append(
                {
                    "d": 0,
                    "enable": 1,
                    "forbidden_port": "",
                    "method": "aes-128-ctr",
                    "obfs": "tls1.2_ticket_auth_compatible",
                    "passwd": password,
                    "port": 6667,
                    "protocol": "auth_aes128_md5",
                    "protocol_param": "",
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
        with open(usersJsonFile, 'r+') as jsonFile:
            users = json.load(jsonFile)
            updateUser = users[id-1]
            updateUser['user'] = user
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
            form.port.data = user['port']
            # print(user)
            return render_template('updateuser.html', form=form)

class UserForm(Form):
    id = IntegerField('Id')
    user = StringField('User')
    port = IntegerField('Port')


if __name__ == '__main__':
    app.run(debug=True)