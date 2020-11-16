###########################
# Imports and Dependancies
###########################
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
#########################
##Connections and Setups
#########################
engine=create_engine("sqlite:///hawaii.sqlite")
Base=automap_base()
Base.prepare(engine,reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
app = Flask(__name__)
#########################
#Flask Routes
#########################
@app.route("/")
def welcome():
    """list all available routes."""
    return( 
        f"Welcome<br/>"
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Temperature: /api/v1.0/tobs<br/>"
        f"Start date: /api/v1.0/<start><br>"
        f"Start and End date: /api/v1.0/<start>/<end><br>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    last_row = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    twelve_months_ago = (dt.datetime.strptime(last_row[0], '%Y-%m-%d') - dt.timedelta(days = 365)).strftime('%Y-%m-%d')
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= twelve_months_ago).all()
    
    session.close()
    all_results = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_results.append(precip_dict)
    
    return jsonify(all_results)
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    station_list = session.query(Station.station).group_by(Station.station).all()
    session.close()
    
    return jsonify(station_list)
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    latest_obvs = session.query(Measurement.date).filter(Measurement.station == "USC00519281").order_by(Measurement.date.desc()).first()
    year_from_latest = (dt.datetime.strptime(latest_obvs[0], '%Y-%m-%d') - dt.timedelta(days = 365)).strftime('%Y-%m-%d')
    dates_temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_from_latest).filter(Measurement.station == "USC00519281").group_by(Measurement.date).order_by(Measurement.date).all()
    
    session.close()
    
    return jsonify(dates_temps)
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start(start, end=""):
    # create session link from Python to the database
    session = Session(engine)
    # Get all tobs results from the given date
    if end == "":
        tobs_result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
        t_result = list(np.ravel(tobs_result))
        return jsonify(t_result)
    else:
        tobs_result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        t_result = list(np.ravel(tobs_result))
        
        return jsonify(t_result)
if __name__ == "__main__":
    app.run(debug=True)