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
        con.row_factory =sqlite3.Row
        
        # Creates a cursor to manage the connections to the database
        cur = con.cursor()

        res = cur.execute(
            'SELECT * FROM tasks;'
        ).fetchall()

        con.close()

        tasks = []
        for row in res:
            tasks.append({
                'description': res[length]['description'],
                'subject': res[length]['subject'],
                'deadline': res[length]['deadline']
            })
        return render_template('index.html', tasks=tasks)
    
    if request.method == 'POST':

        return render_template('index.html', tasks=tasks)




    return render_template('index.html')

@app.route('/addSubject', methods=['GET', 'POST'])
def addSubject():
    return render_template('addSubject.html')


