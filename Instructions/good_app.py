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
#session = Session(engine) 
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
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start date/end date" 
)

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

# Calculate the date 1 year ago from the last data point in the database
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

# Query for the last 12 months of precipitation data
    last_twelve_months = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()
    
# Convert query results to a dictionary using date as the key and prcp as the value
    precip_dict = precip_dict = {date : prcp for date, prcp in last_twelve_months}
    session.close()

# Return the JSON representation of your dictionary
    print("Loaded precip query")
    return jsonify(precip_dict)

# Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

# Query Stations
    results = session.query(Station)

# List results in dictionary format so we can jsonify the list of stations
    stations_list = []
    for station in results:
        station_dict = {}
        station_dict['station'] = station.station
        station_dict['name'] = station.name
        stations_list.append(station_dict)

        session.close()

    print ("Stations available")
    return jsonify(stations_list)
 

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Calculate the date 1 year ago from the last data point in the database
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

    #Query the dates and temperature observations of the most active station for the last year of data
    top_station_obs = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= year_ago).all()

    #Use numpy ravel function to extract all individual temp observations from top_station-Obs variable and allow us to store them somewhere else so that we can use them in a list.
    all_tobs = list(np.ravel(top_station_obs))

    session.close()

    print ("Last 12 months of temperature observations from the most active station")
    return jsonify(all_tobs)

@app.route("/api/v1.0/start/<start_date>")
def start(start_date):
    session = Session(engine)
# Find the minimum temp, average temp, and maximum temp for all tobs 
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)] 

    temp_range = session.query(*sel).filter(Measurement.date >= start_date).all()
   
    #Use numpy ravel function to extract all individual temp observations from top_station-Obs variable and allow us to store them somewhere else so that we can use them in a list.
    temp_ranges = list(np.ravel(temp_range))

    session.close()
    return jsonify(temp_ranges) 

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    session = Session(engine)
# Find the minimum temp, average temp, and maximum temp for all tobs 
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    temp_range = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    #Use numpy ravel function to extract all individual temp observations from top_station-Obs variable and allow us to store them somewhere else so that we can use them in a list.
    temp_ranges = list(np.ravel(temp_range))

    session.close()
    return jsonify(temp_ranges) 

if __name__== "__main__":
    app.run(debug=True)