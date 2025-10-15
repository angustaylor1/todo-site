from flask import Flask, render_template, session, request, redirect
import sqlalchemy as db

# This creates the engine object that acts as a central source
# of connections for the database
engine = db.create_engine('sqlite+pysqlite:///:memory:')
connection = engine.connect()

#  This creates the metadata object that contains
#  the information about the tables and columns
# that are contained in the database
metadata = db.MetaData()


# create the two tables with their columns
tasks = db.Table(
    'tasks',
    metadata,
    db.Column('id', db.Integer, primary_key=True, nullable=False, autoincrement=True),
    db.Column('description', db.String(200)),
    db.Column('subject', db.String(50)),
    db.Column('subject_id', db.ForeignKey('subjects.id'), nullable=False)
)
subjects = db.Table(
    'subjects',
    metadata,
    db.Column('id', db.Integer, primary_key=True, nullable=False, autoincrement=True),
    db.Column('subjectName', db.String)
)

stmt = db.insert(subjects).values(subjectName='Miscellaneous')

# This initializes and creates the tables into existence
metadata.create_all(engine)

app = Flask(__name__)


def apology(message):
    return render_template('apology.html', message=message)




@app.route('/', methods =['GET', 'POST'])
def index():

    if request.method == 'POST':
        # get info from the table
        description = request.form.get('description')
        deadline = request.form.get('deadline')
        subject = request.form.get('subject')

        # create statement to get subject id for update.
        get_sub_id = db.select(subjects).where(subjects.subjectName == subject)
        subject_id = connection.execute(get_sub_id)

        insert_task = db.insert(subjects).values(
            description=description,
            deadline=deadline,
            subject=subject,
            subject_id=subject_id
        )
        try:
            connection.execute(insert_task)
        except:
            return "Coulnd't update the table"
        return redirect('/')


    get_task_info = db.select(tasks)
    tasks = connection.execute(get_task_info)

    return render_template('index.html', tasks=tasks)


