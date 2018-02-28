from flask import Flask, render_template, request, redirect
from flask import jsonify
from wtforms import Form,StringField
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


@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    form = UserForm(request.form)
    if(request.method == 'POST'):
        user = form.user.data
        # print(user.data)

        with open(usersJsonFile, 'r+') as jsonFile:
            users = json.load(jsonFile)
            users[1]['user'] = user
            jsonFile.seek(0)  # rewind
            json.dump(users, jsonFile)
            jsonFile.truncate()
            return redirect('/') 

    return render_template('adduser.html', form=form)


class UserForm(Form):
    user = StringField('User')


if __name__ == '__main__':
    app.run(debug=True)