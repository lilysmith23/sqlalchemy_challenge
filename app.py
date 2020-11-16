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
