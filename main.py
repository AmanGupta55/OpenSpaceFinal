from flask import Flask
from flask import request, render_template, jsonify, flash, redirect, url_for
import json
from datetime import datetime
from wtforms import Form, DateTimeField, IntegerField, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    field = StringField('What Field do you Want', [validators.DataRequired()])
    people = IntegerField('How many people on the field', [validators.DataRequired()])
    startdatetime = DateTimeField('What time do you want the field', [validators.DataRequired()])
    enddatetime = DateTimeField('What time will you be off the field', [validators.DataRequired()])
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

class User():
    def __init__(self, name, email, field, people, startdatetime, enddatetime):
        self.name = name
        self.email = email
        self.field = field
        self.people = people
        self.startdatetime = startdatetime
        self.enddatetime = enddatetime

    def dumpJson(self):
        data = []
        with open('events.json', "r") as json_file:
            data = json.load(json_file)

        data.append({
            "title": self.field + "\n Name: " + self.name + "\n Email: " + self.email + "\n People: " + str(self.people),
            "start": self.startdatetime.strftime("%m-%d-%Y %H:%M:%S+13:21"),
            "end": self.enddatetime.strftime("%m-%d-%Y %H:%M:%S+13:21")
        })

        with open('events.json', 'w') as outfile:
            json.dump(data, outfile)

app = Flask(__name__)
app.secret_key = 'super secret key'


@app.route('/')
def calendar():
    return render_template("json.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/data')
def return_data():
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')
    with open("events.json", "r") as input_data:
        return input_data.read()

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.name.data, form.email.data, form.field.data, form.people.data, form.startdatetime.data, form.enddatetime.data)
        user.dumpJson()
        flash('Thanks for booking a field')
        return redirect('/login')
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.debug = True
    app.run()
