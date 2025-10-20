from flask import Flask, render_template, session, request, redirect # type: ignore
import sqlite3
from info import getAllTasks, getSubjectNames, apology

app = Flask(__name__)


def apology(message):
    return render_template('apology.html', message=message)

def getSubjectNames():
    con = sqlite3.connect('todosite.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    result = cur.execute(
        "SELECT subject_name FROM subjects;"
        ).fetchall()
    subjects = []
    for row in result:
        subjects.append({
        'subject': row['subject_name']
        })


    con.close()
    return subjects

def getAllTasks():
    con = sqlite3.connect('todosite.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    res = cur.execute(
        'SELECT * FROM tasks ORDER BY deadline;'
    ).fetchall()

    tasks = []
    for row in res:
        tasks.append({
            'id': row['task_id'],
            'description': row['description'],
            'subject': row['subject'],
            'deadline': row['deadline']
        })

    con.close()
    return tasks


@app.route('/', methods =['GET', 'POST'])
def index():

    if request.method == 'GET':
        tasks = getAllTasks()
        subjects = getSubjectNames()

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
            return '<h1>Please enter a description</h1>'
        elif not deadline:
            return'<h1>Please enter a deadline</h1>'
        elif not subject:
            return'<h1>Please choose a subject</h1>'
        res = cur.execute(
            'SELECT subject_id FROM subjects WHERE subject_name = ?;', (subject,)
        )
        subject_id = []
        for row in res:
            subject_id.append({
                'id': row['subject_id']
            })
        
        cur.execute(
            'INSERT INTO tasks (description, subject, deadline, subject_id) VALUES (?, ?, ?, ?);',
            (description, subject, deadline, subject_id[0]['id'])
            )
        con.commit()
        con.close()
        return redirect('/')        

@app.route('/addSubject', methods=['GET', 'POST'])
def addSubject():

    if request.method == "GET":
        con = sqlite3.connect('todosite.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        res = cur.execute(
            'SELECT subject_name FROM subjects;'
        ).fetchall()
        con.close()
        subjects = []

        for row in res:
            subjects.append({
                'subject': row['subject_name']
            })
            
        return render_template('addSubject.html', subjects=subjects)
    
    if request.method == 'POST':

        newSubjectName = request.form.get('subject_name')
        subjectColor = request.form.get('color')

        if not newSubjectName:
            return '<h1>Make sure the subject has a name'
        elif not subjectColor:
            return '<h1>Make sure to select a color</h1?'
        
        con = sqlite3.connect('todosite.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        subject_names = cur.execute(
            'SELECT subject_name FROM subjects'
        ).fetchall()

        for row in subject_names:
            if row['subject_name'] == newSubjectName:
                return 'That subject name is already created. Try another one.'

        try:
            res = cur.execute(
                'INSERT INTO subjects (subject_name, subject_color) VALUES (?, ?);',
                (newSubjectName, subjectColor)
            )
            con.commit()
            con.close()
            return render_template('addSubject.html', message='Succesfully created new Subject!')
        except:
            con.close()
            return '<h1> We couldn\'t create that subject</h1>'


@app.route('/deleteSubject', methods=['GET', 'POST'])
def deleteSubject():
        if request.method == "GET":
            con = sqlite3.connect('todosite.db')
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            res = cur.execute(
                'SELECT subject_name FROM subjects;'
            ).fetchall()
            subjects = []

            for row in res:
                subjects.append({
                    'subject': row['subject_name']
                })

            return render_template('deleteSubject.html', subjects=subjects)
        
        if request.method == 'POST':
            subject = request.form.get('subject')

            con = sqlite3.connect('todosite.db')
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            if  not subject:
                con.close()
                return apology('Please choose a subject to delete.')

            try:
                cur.execute(
                    'DELETE FROM tasks WHERE subject_id = (SELECT subject_id FROM subjects WHERE subject_name = ?)', (subject,)
                )
                con.commit()
                cur.execute(
                    'DELETE FROM subjects WHERE subject_name = ?;',
                    (subject,)
                )
                con.commit()
                con.close()
                return redirect('/deleteSubject')
            except:
                con.close()
                return redirect('/deleteSubject')

@app.route('/completeTask/<int:id>')
def deleteTask(id):
        con = sqlite3.connect('todosite.db')
        cur = con.cursor()

        cur.execute(
            'DELETE FROM tasks WHERE task_id = ?;', (id,)
        )
        con.commit()
        con.close()

        return redirect('/') 


@app.route('/updateTask/<int:id>', methods =['GET', 'POST'])
def updateTask(id):
    if request.method == "GET":
            con = sqlite3.connect('todosite.db')
            con.row_factory = sqlite3.Row
            cur = con.cursor()


            res = cur.execute(
                'SELECT * FROM tasks WHERE task_id = ?', (id,)
            ).fetchone()
            task = {
                'description': res['description'],
                'deadline': res['deadline'],
                'subject': res['subject']
            }
            result = cur.execute(
                "SELECT subject_name FROM subjects;"
            ).fetchall()
            
            subjects = []
            
            for row in result:
             subjects.append({
                'subject': row['subject_name']
            })

            
            con.close()
            
            return render_template('update.html', task=task, subjects=subjects)



