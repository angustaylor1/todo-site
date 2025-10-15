from flask import Flask, render_template, session, request
import sqlalchemy as db
from sqlalchemy import select


app = Flask(__name__)

engine = db.create_engine('sqlite:///database.db')
connection = engine.connect()

metadata = db.MetaData()

user_table = db.Table(
    'users',
    metadata,
    db.Column('user_id', db.Integer, primary_key=True),
    db.Column('username', db.String),
    db.Column('password', db.String)
)

def select_all_data(table_name):
    query = table_name.select()
    result = connection.execute(query)
    return result.all()

def apology(message):
    return render_template('apology.html', message=message)





@app.route('/')
def idex():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        user = request.get('exampleEmailInput1')
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    return

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['registerUsername']
        password1 = request.form['registerPassword1']
        password2 = request.form['registerPassword2']

        info = select_all_data(user_table)
        for row in info:
            if username == row['username']:
                return apology("Username is taken")


        # we need to get a list of the usernames and passwords.


        return render_template('register.html')


