from flask import Flask, render_template, session, request, redirect, jsonify # type: ignore
import sqlite3
from info import getAllTasks, getSubjectNames, apology, getSubjectID, getAllSubjectInfo



app = Flask(__name__)



@app.route('/', methods =['GET', 'POST'])
def index():

    if request.method == 'GET':
        tasks = getAllTasks()
        subjects = getAllSubjectInfo()
        

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
            'SELECT subject_name, subject_color FROM subjects;'
        ).fetchall()
        con.close()
        subjects = []

        for row in res:
            subjects.append({
                'subject': row['subject_name'],
                'subject': row['subject_color']
            })
            
        return render_template('addSubject.html', subjects=subjects)
    
    if request.method == 'POST':

        newSubjectName = request.form.get('subject_name')
        subjectColor = request.form.get('subject_color')

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
            subjects = getSubjectNames()
            return render_template('deleteSubject.html', subjects=subjects)
        
        if request.method == 'POST':
            subject = request.form.get('subject')

            con = sqlite3.connect('todosite.db')
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            
            # check the user chose a subject
            if  not subject:
                con.close()
                return apology('Please choose a subject to delete.')
            
            # get the subject names to check the subject exists.
            subjects = getSubjectNames()

            # check if the chosen subject exists
            # if it does we carry on, if it doesn't
            # we send an error.
            found = False
            for elem in subjects:
                if elem['subject'] == subject:
                    found = True
                    break

            if not found:
                con.close()
                return apology('That subject doesn\'t exist so can\'t be deleted')

            
            # we have confirmed the subject exists, so we can delete it and its tasks
            try:
                # delete all of the tasks related to chosen subject
                cur.execute(
                    'DELETE FROM tasks WHERE subject_id = (SELECT subject_id FROM subjects WHERE subject_name = ?)', (subject,)
                )
                con.commit()

                # delete the subject from subject table.
                cur.execute(
                    'DELETE FROM subjects WHERE subject_name = ?;',
                    (subject,)
                )
                con.commit()
                con.close()
                return redirect('/deleteSubject')
            except:
                con.close()
                return '<h1>Could not delete that subject</h1>'

@app.route('/completeTask/<int:id>')
def completeTask(id):
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
                'id': res['task_id'],
                'description': res['description'],
                'deadline': res['deadline'],
                'subject': res['subject']
            }
            
            subjects = getSubjectNames()

            con.close()
            
            return render_template('update.html', task=task, subjects=subjects)
    
    if request.method == 'POST':

        # get the form input info.
        description = request.form.get('description')
        deadline = request.form.get('deadline')
        subject = request.form.get('subject')

        # check the info is sound
        if not description:
            return '<h1>Please enter a description</h1>'
        elif not deadline:
            return'<h1>Please enter a deadline</h1>'
        elif not subject:
            return'<h1>Please choose a subject</h1>'

        # collect the subject ID
        subject_id = getSubjectID(subject)

        # ensure the subject exists
        if not subject_id:
            return apology('That Subject does not exist')

        # connect to db
        con = sqlite3.connect('todosite.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # try to update the database, if it doesnt wrok throw an error.
        try:
            cur.execute(
                'UPDATE tasks SET description = ?, subject = ?, deadline = ?, subject_id = ? WHERE task_id = ?',
                (description, subject, deadline, subject_id, id,)
            )
            # VERY IMPORTANT COMMIT THE CHANGES SO THEY ACTUALLY HAPPEN
            con.commit()
            con.close()
        except:
            con.close()
            return '<h1> Sorry brother couldnt update that for you.</h1>'

        # return redirect to index and the table should be altered.
        return redirect('/')



