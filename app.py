# Dependencies
import datetime as dt
import numpy as np
import pandas as pd

# Dependencies needed for SQLAlchemy 
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Dependencies needed for Flask
from flask import Flask, jsonify

# Access the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

# Function to access and query SQLite database file
Base = automap_base()

# Reflect database
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session link from Python to database
session = Session(engine)

# Set up Flask
app = Flask(__name__)

# Define welcome route
@app.route('/')

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API! </br>
    Available Routes: <br/>
    /api/v1.0/precipitation <br/>
    /api/v1.0/stations <br/>
    /api/v1.0/tobs <br/>
    /api/v1.0/temp/start/end <br/>
    ''')

# Define precipitation route
@app.route('/api/v1.0/precipitation')

def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Define stations route
@app.route('/api/v1.0/stations')

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

# Define monthly temperature route
@app.route('/api/v1.0/tobs')

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    
    temps = list(np.ravel(results))
    
    return jsonify(temps)

# Define statistics route
@app.route('/api/v1.0/temp/<start>')
@app.route('/api/v1.0/temp/<start>/<end>')

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).\
        filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)