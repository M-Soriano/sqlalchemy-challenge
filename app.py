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
    
    #covertquery to dictionary 
    perc_data= {date: prcp for date, prcp in precipitation_data}
    return jsonify(perc_data)

@app.route(/api/v1.0/stations)



if __name__=='__main__':
    app.run(debug=True)