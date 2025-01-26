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
#engine= create_engine('sqlite:///hawaii.sqlite')


# reflect an existing database into a new model
#Base= automap_base()
# reflect the tables
#Base.prepare(autoload_with=engine)

# Save references to each table
#measurements=Base.classes.measurement
#stations=Base.classes.station

# Create our session (link) from Python to the DB
#ession=Session(engine)

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
        <a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a>
        <a href="/api/v1.0/stations">/api/v1.0/stations</a>
        <a href="/api/v1.0/tobs">/api/v1.0/tobs</a>
        <a href="/api/v1.0/<start>">/api/v1.0/<start></a>
        <a href="/api/v1.0/<start>/<end>">/api/v1.0/<start>/<end></a>
    </body>
    </html>
"""
    return routes   

@app.route("/api/v1.0/precipitation")
def precipitation():
    return(f"works I guess")

if __name__=='__main__':
    app.run(debug=True)