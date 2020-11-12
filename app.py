from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home(): 
    print("Server received request for home page")
    return (
        f"These are the routes available:"       
        
        f"/api/v1.0/precipitation"
        
        f"/api/v1.0/stations"
        
        f"/api/v1.0/tobs"
        
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation_levels():

    session = Session(engine)
    results = session.query(*columns).filter(Measurement.date >= twelve_months_ago).all()
    session.close()

    for date, prcp in results:
        precipitation_dict = {}
        passenger_dict["date"] = date
        passenger_dict["prcp"] = prcp
    return jsonify(precipitation_dict)    

@app.route("/api/v1.0/stations")
def stations_list():

    session = Session(engine)
    station_list = station_count
    session.close()
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temperature_obvservations():
    
    session = Session(engine)
    temp_station = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= year_ago).\
    filter(Measurement.station == "USC00519281").\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()
    session.close()
    return jsonify(temp_station)

# @app.route("/api/v1.0/<start> and /api/v1.0/<start>/<end>")
# def min_max_avg_temperature():
#     return ""