from flask import Flask, render_template, session, request
import sqlalchemy as db

# This creates the engine object that acts as a central source
# of connections for the database
engine = db.create_engine('sqlite+pysqlite:///:memory:')

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
    db.Column('Subject Name', db.String)
)

# This initializes and creates the tables into existence
metadata.create_all(engine)

app = Flask(__name__)


def apology(message):
    return render_template('apology.html', message=message)




@app.route('/', methods =['GET', 'POST'])
def index():
    if request.method == 'POST':
        description = request.form.get('description')
        deadline = request.form.get('deadline')
        subject = request.form.get('subject')

    return render_template('index.html')


