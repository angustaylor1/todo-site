from flask import render_template
import sqlite3

# function that creates a page for any errors encouuntered
def apology(message):
    return render_template('apology.html', message=message)

# function retrieves all of the existing
# subject names and returns them in a list of dicts.
def getSubjectNames():
   
    # connects to database and creates a cursor
    con = sqlite3.connect('todosite.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    # retrieves the data from the db
    result = cur.execute(
        "SELECT subject_name FROM subjects;"
        ).fetchall()
    
    # populates subjects with a list of dicts of all the subject names
    subjects = []
    for row in result:
        subjects.append({
        'subject': row['subject_name']
        })
        # closes connection
    con.close()

    return subjects

# function that returns all the current tasks in the database
def getAllTasks():
    con = sqlite3.connect('todosite.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    # gets the data from db
    res = cur.execute(
        'SELECT * FROM tasks ORDER BY deadline;'
    ).fetchall()

    # populates tasks with a list of dicts with all of the task info.
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



def getAllSubjectInfo():
    # connects to database and creates a cursor
    con = sqlite3.connect('todosite.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    # retrieves the data from the db
    result = cur.execute(
        "SELECT subject_name, subject_color FROM subjects;"
        ).fetchall()
    
    # populates subjects with a list of dicts of all the subject names
    subjects = []
    for row in result:
        subjects.append({
        'subject': row['subject_name'],
        'color': row['subject_color']
        })
        # closes connection
    con.close()

    return subjects


def getSubjectID(subject):
    con = sqlite3.connect('todosite.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    res = cur.execute(
        'SELECT subject_id FROM subjects WHERE subject_name = ?', (subject,)
    ).fetchone()
    
    con.close()
    
    if res:
        return res['subject_id']
    else:
        return None