import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
#import climate_starter.ipynb
import pandas as pd
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create our session (link) from Python to the DB
session = Session(engine) 
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    print("Server received request for 'Home' page...")

    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>" 
)

@app.route("/about")
def about():
    print("Loaded 'about'")
    return "Madison, Clarksville TN"

@app.route("/api/v1.0/precipitation")
def precipitation():
# Calculate the date 1 year ago from the last data point in the database
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

# Query for the last 12 months of precipitation data
    last_twelve_months = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()
    
# Convert query results to a dictionary using date as the key and prcp as the value
    precip_dict = precip_dict = {date : prcp for date, prcp in last_twelve_months}
# Return the JSON representation of your dictionary
    print("Loaded precip query")
    return jsonify(precip_dict)

# Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
# Query Stations
#    station_query = session.query(Station)
    results = session.query(Station)

# List results in dictionary format so we can jsonify the list of stations
    stations_list = []
    for station in results:
        station_dict = {}
        station_dict['Station'] = station
        station_dict['Name'] = name
        stations_list.append(station_dict)

#    print("Stations available")
#    return "Stations available"
    return jsonify(stations_list)


#@app.route("/api/v1.0/tobs")
#def tobs():
#    print("")
#    return("")


#@app.route("")




if __name__=="__main__":
    app.run(debug=True)