from flask import Flask, render_template, session, request, redirect
import sqlite3


app = Flask(__name__)


def apology(message):
    return render_template('apology.html', message=message)




@app.route('/', methods =['GET', 'POST'])
def index():

    if request.method == 'GET':
        # creates a connection to the database
        con = sqlite3.connect('todosite.db')
        
        # returns the data in the form of dicts so column names can be accessed
        # (otherwise it comes as a tuple that can't be accessed with column names)
        con.row_factory = sqlite3.Row
        
        # Creates a cursor to manage the connections to the database
        cur = con.cursor()

        res = cur.execute(
            'SELECT * FROM tasks;'
        ).fetchall()

        tasks = []
        for row in res:
            tasks.append({
                'description': row['description'],
                'subject': row['subject'],
                'deadline': row['deadline']
            })

        result = cur.execute(
            "SELECT subject_name FROM subjects;"
        ).fetchall()
        subjects = []
        for row in result:
            subjects.append({
                'subject': row['subject_name']
            })

        return render_template('index.html', tasks=tasks, subjects=subjects)
    
    if request.method == 'POST':
        # connect to database
        con = sqlite3.connect('todosite.db')

        # allow data to be dicts
        con.row_factory = sqlite3.Row

        # connect cursor
        cur = con.cursor()

        description = request.form.get('description')
        deadline = request.form.get('deadline')
        subject = request.form.get('subject')

        if not description:
            return '<h1>Please enter a description<h1>'
        elif not deadline:
            return'<h1>Please enter a deadline<h1>'
        elif not subject:
            return'<h1>Please choose a subject<h1>'
        
        
        cur.execute(
            'INSERT INTO tasks (description, subject, deadline) VALUES (?, ?, ?)',
            (description, subject, deadline)
            )
        con.commit()
        con.close()
        return redirect('/')        

@app.route('/addSubject', methods=['GET', 'POST'])
def addSubject():
    return render_template('addSubject.html')


