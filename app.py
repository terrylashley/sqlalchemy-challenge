#Import needed dependencies
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import sqlalchemy
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

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Routes
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def rain():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #What is the latest date
    latest_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    #index into the object created from the "latest_date"
    latest_date = latest_date[0]
    # Calculate the date 1 year ago from the last data point in the database
    last_year = dt.datetime.strptime(latest_date, "%Y-%m-%d") - dt.timedelta(days=366)

    """Convert the query results to a Dictionary using `date` as the key and `prcp` as the value """
    # Query all passengers
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= last_year).all()

    session.close()

    # create a dictionary from the data
    
    percipitation_dict = {}
    for date, prcp in results:
        
        percipitation_dict[date] = prcp    
        
    return jsonify(percipitation_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset"""
    # Query 
    results = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    sessions_list = []
    for i in results:
        
        
        sessions_list.append(i)

    return jsonify(sessions_list)

@app.route("/api/v1.0/tobs")
def temps():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    temp_list=[]
    results = session.query(measurement.tobs).filter(measurement.date >= year_ago).all()
    """* query for the dates and temperature observations from a year from the last data point.
  * Return a JSON list of Temperature Observations (tobs) for the previous year."""
    session.close()
        
    for i in results:
        temp_list.append(i)
  
      return jsonify(temp_list)

    
if __name__ == '__main__':
    app.run(debug=False)

