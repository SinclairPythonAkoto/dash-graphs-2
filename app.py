import os

from flask import Flask, render_template, url_for, request, redirect, flash
import dash
import dash_core_components as dcc
import dash_html_components as html

server = Flask(__name__)

server.secret_key = os.getenv("SECRET_KEY")


from sqlalchemy.orm import sessionmaker, relationship

# # this part is needed to create session to query database.  this should be JUST BELOW app.config..
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, select
meta = MetaData()
engine = create_engine(os.getenv("DATABASE_URL"), echo = True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# database here
class DashGraphs(Base):
    __tablename__ = 'dash_graphs'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(20))
    f_visit = Column('first_visit', String(3))
    comeback = Column('visit_again', String(3))

    def __init__(self, name, f_visit, comeback):
        self.name = name
        self.f_visit = f_visit
        self.comeback = comeback

Session = sessionmaker(bind=engine)
db_session = Session()

title = "Dash Graphs"

@server.route('/')
def home():
    return render_template('home.html')

@server.route('/insert_data', methods=['GET', 'POST'])
def insert_data():
    if request.method == 'GET':
        return render_template('insert_data.html', title=title)
    else:
        name = request.form.get("username")
        firstVisit = request.form.get("first_visit")
        visit = request.form.get("visited")
        visitAgain = request.form.get("visit_again")

        db_entry = DashGraphs(name, firstVisit, visit, visitAgain)
        db_session.add(db_entry)
        db_session.commit()
        flash(f'Thank you {name} for your info!')
        return render_template('insert_data.html')

# create ALL X axis first
def X_fv_yes():
    ''' finds all the entries == yes in first_visit column '''
    ''' this converts ['yes','yes','yes'] to 3 '''
    ''' X axis for graph '''
    fv_data_yes = db_session.query(DashGraphs).filter(DashGraphs.f_visit=="yes").all()
    val = int(len([fv.f_visit for fv in fv_data_yes]))
    return val

def X_fv_no():
    ''' finds all the entries == yes in first_visit column '''
    ''' this converts ['no','no','no'] to 3 '''
    ''' X axis for graph '''
    fv_data_no = db_session.query(DashGraphs).filter(DashGraphs.f_visit=="no").all()
    val = int(len([fv.f_visit for fv in fv_data_no]))
    return val

def X_visit_again_yes():
    ''' finds all the entries == yes in visit_again column '''
    ''' X axis for graph '''
    return_yes = db_session.query(DashGraphs).filter(DashGraphs.comeback=="yes").all()
    val = len([r.comeback for r in return_yes])
    return val

def X_visit_again_no():
    ''' finds all the entries == no in visit_again column '''
    ''' X axis for graph '''
    return_no = db_session.query(DashGraphs).filter(DashGraphs.comeback=="no").all()
    val = len([r.comeback for r in return_no])
    return val


# now create ALL Y axis
def Y_fv_yes():
    ''' calculates all the entries == yes in first_visit column and puts them in a list'''
    ''' The list counts from [0, 1, 2 etc] '''
    ''' Y axis for graph '''
    fv_data_yes = db_session.query(DashGraphs).filter(DashGraphs.f_visit=="yes").all()
    val = int(len([fv.f_visit for fv in fv_data_yes]))
    return val

def Y_fv_no():
    ''' calculates all the entries == yes in first_visit column and puts them in a list'''
    ''' The list counts from 0, 1, 2 etc '''
    ''' Y axis for graph '''
    fv_data_no = db_session.query(DashGraphs).filter(DashGraphs.f_visit=="no").all()
    val = int(len([fv.f_visit for fv in fv_data_no]))
    return val


def Y_visit_again_yes():
    ''' calculates all the entries == yes in first_visit column and puts them in a list'''
    ''' The list counts from 0, 1, 2 etc '''
    ''' Y axis for graph '''
    return_yes = db_session.query(DashGraphs).filter(DashGraphs.comeback=="yes").all()
    val = int(len([r.comeback for r in return_yes]))
    return val

def Y_visit_again_no():
    ''' calculates all the entries == no in first_visit column and puts them in a list'''
    ''' The list counts from 0, 1, 2 etc '''
    ''' Y axis for graph '''
    return_no = db_session.query(DashGraphs).filter(DashGraphs.comeback=="no").all()
    val = int(len([r.comeback for r in return_no]))
    return val

@server.route('/viewdata')
def viewdata():
    db_data = db_session.query(DashGraphs).order_by(DashGraphs.id)
    data = db_data.all()
    return render_template('viewdata.html', title=title, data=data)

app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/dash/'
)

app.layout = html.Div(children=[
    html.H1(children='Dash Graphs'),

    html.Div(children='''
        Dash Graphs: A simple web app that displays data from a PostgreSQL database.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [X_fv_yes()], 'y': [Y_fv_yes()], 'type': 'bar', 'name': 'Regular Visitors'},
                {'x': [X_fv_no()], 'y': [Y_fv_no()], 'type': 'bar', 'name': 'New Vistors'},
                {'x': [X_visit_again_yes()], 'y': [Y_visit_again_yes()], 'type': 'bar', 'name': 'Would Return'},
                {'x': [X_visit_again_no()], 'y': [Y_visit_again_no()], 'type': 'bar', 'name': 'Would Not Return'},
            ],
            'layout': {
                'title': 'Dash Graphs Number of Visitors'
            }
        },
    ),
    html.Div('''
        This is a random message # place anchor tag here to return home
    '''),
])


if __name__ == '__main__':
    app.run_server(debug=True)