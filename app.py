# Import the dependencies.
import numpy as np
import datetime as dt
import pandas as pd
import sqlalchemy
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base= automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement=Base.classes.measurement
station=Base.classes.station

# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")

def root():#helpful https://python-web.teclado.com/section07/lectures/02_render_template_to_send_longer_strings/
    "Home page with list of routes"

    routes= """
    <html>
    <body>
        <h1>Available routes:</h1>

        <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
        <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
        <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
        <li><a href="/api/v1.0/<start>">/api/v1.0/<start></a></li>
        <li><a href="/api/v1.0/<start>/<end>">/api/v1.0/<start>/<end></a></li>
    </body>
    </html
"""
   
    return routes   


@app.route("/api/v1.0/precipitation")
def precipitation():
    most_recent_date=session.query(measurement.date).order_by(measurement.date.desc()).first()
    one_year_ago= dt.datetime.strptime(most_recent_date[0],"%Y-%m-%d") - dt.timedelta(days=365)
    precipitation_data=session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_ago).all()

    session.close()
    
    #covertquery to dictionary 
    perc_data_dict= {date: prcp for date, prcp in precipitation_data}
    return jsonify(perc_data_dict)

@app.route('/api/v1.0/stations')
def stations():
    stationlist=session.query((func.distinct(station.station))).all()
    #converting to list
    station_data_list=[station[0] for station in stationlist]

    return jsonify(station_data_list)

@app.route("/api/v1.0/tobs")
def tobs():
    most_recent_date=session.query(measurement.date).order_by(measurement.date.desc()).first()
    one_year_ago= dt.datetime.strptime(most_recent_date[0],"%Y-%m-%d") - dt.timedelta(days=365)
    station_activity=session.query(measurement.station,func.count())\
        .group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    station_active_date_temp=session.query(measurement.date, measurement.tobs)\
        .filter(measurement.station == station_activity[0][0], measurement.date >= one_year_ago).all()
    #Only putting temparute in list becuase that is the only variable asked in the instruction
    templist= [tobs[1] for tobs in station_active_date_temp]

    return jsonify(templist)

    
    





if __name__=='__main__':
    app.run(debug=True)

