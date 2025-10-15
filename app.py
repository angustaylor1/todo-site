from flask import Flask, render_template, session, request
# import sqlalchemy as db



# metdata_obj = db.MetaData()



app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)
# connection = engine.connect()

# users = db.Table(
#     'user',
#     metadata_obj,
#     db.Column(db.Integer, primary_key=True),
#     db.Column('email', db.String),
#     db.Column('password', db.String)
# )


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
        email = request.form['registerEmail']
        password1 = request.form['registerPassword1']
        password2 = request.form['registerPassword2']

        # check if the email is already in use
        # if it is we fail and say email already exists
        # if not check the passwords are the same
        # if not we say the passwords have to be the same
        # if it is then we update the database, tell them that its succesful and say log in.


        return render_template('register.html')


