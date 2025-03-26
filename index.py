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
session=Session(bind=engine)

#global variable and functions to a
most_recent_date=session.query(measurement.date).order_by(measurement.date.desc()).first()[0]

oldest_date=session.query(measurement.date).order_by(measurement.date.desc()).all()[-1][0]
session.close()

def one_year_ago_func(date):
    one_year= dt.datetime.strptime(date,"%Y-%m-%d") - dt.timedelta(days=365)
    session.close()
    return (one_year)

def precipitation_data_func(date):
    filter_data =session.query(measurement.date, measurement.prcp).filter(measurement.date >= date).all()
    session.close()
    return (filter_data)

def datesearch_func(start,end):
    
    if end <= most_recent_date and start >= oldest_date and start <= most_recent_date:
        date_search = session.query(
            func.min(measurement.tobs), 
            func.max(measurement.tobs),
            func.avg(measurement.tobs)).filter(measurement.date >= start)
        session.close()
        return date_search
    
    else:
        return "check_data"
def makelist_func(datasearch):
    startlist=[]
    for min,max,avg in datasearch:
        temp_data={}
        temp_data["min"]=min
        temp_data['max']=max
        temp_data['avg']=avg
        startlist.append(temp_data)
    return startlist

def checking_func(dates):
    try:
        bool(dt.datetime.strptime(dates,"%Y-%m-%d"))   
    except ValueError:
        dates="faulty"
        return dates
    

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
        <li ><strong>Following routes must be manually pasted on address bar and dates select</strong></li>
        <li><a >/api/v1.0/&ltstart></a></li>
        <li><a >/api/v1.0/&ltstart>/ &ltend></a></li>
    </body>
    </html
"""
   
    return routes   


@app.route("/api/v1.0/precipitation")
def precipitation():
    #function call for global function
    one_year_ago=one_year_ago_func(most_recent_date)
    precipitation_data= precipitation_data_func(one_year_ago)
    #-----
    session.close()
    
    #covertquery to dictionary 
    perc_data_dict= {date: prcp for date, prcp in precipitation_data}
    return jsonify({"Precipitation Analysis":f"12 Month of Data from {one_year_ago} to {most_recent_date}"},perc_data_dict)

@app.route('/api/v1.0/stations')
def stations():
    #stationlist=session.query(func.distinct(stations.station)).all()
    stationlist=session.query(func.distinct(station.station))\
    .join(measurement, station.station == measurement.station).all()
    session.close()
    #converting to list
    station_data_list=[station[0] for station in stationlist]
  

    return jsonify({"Stations list":"From dataset"},station_data_list)

@app.route("/api/v1.0/tobs")
def tobs():
    one_year_ago=one_year_ago_func(most_recent_date)

    #query only mesurement table since it has of the temperature and date data
    station_activity=session.query(measurement.station,func.count())\
        .group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    station_active_date_temp=session.query(measurement.date, measurement.tobs)\
        .filter(measurement.station == station_activity[0][0], measurement.date >= one_year_ago).all()
    session.close()
    #Only putting temparute in list becuase that is the only variable asked in the instruction
    templist= []
    for date, tobs in station_active_date_temp:
        date_tobs_dict={}
        date_tobs_dict['date'] = date
        date_tobs_dict['tobs'] = tobs
        templist.append(date_tobs_dict)

    return jsonify({f'The most active station is {station_activity[0][0]}':
     f'Date and temperature data for this station:'}, templist)

@app.route("/api/v1.0/<start>")
def start(start):
    
    #helpful for checking format https://www.geeksforgeeks.org/python-validate-string-date-format/
    result=checking_func(start)
    if result == "faulty":
        return jsonify({"error": f"Check that your date is formatted correctly. Year-month-day(2010-12-12)"})
    else:
        date_search= datesearch_func(start,most_recent_date)
        if date_search == "check_data":
                return jsonify({"error": f"Check that your date is between {oldest_date} and {most_recent_date}"})
        else:
            startlist=makelist_func(date_search)
            return jsonify(f"Data from {start} to {most_recent_date}",startlist)

@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):

    result = checking_func(start)
    result2 = checking_func(end)
    if result == "faulty" or result2 == "faulty":
        return jsonify({"error": f"Check that your date is formatted correctly. Year-month-day(2010-12-12)"})
    else:
        if start > end:
            return jsonify({"error":"The start date must be before the end date"})
        else:
            data_search=datesearch_func(start,end)
            if data_search =="check_data":
                return jsonify({"error": f"Check that your date is between {oldest_date} and {most_recent_date}"})
            else:
                startlist=makelist_func(data_search)
                return jsonify(f"Data from {start} to {end}",startlist)



if __name__=='__main__':
    app.run(debug=True)

