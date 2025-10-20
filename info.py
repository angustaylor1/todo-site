from flask import Flask, render_template, session, request, redirect # type: ignore
import sqlite3


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