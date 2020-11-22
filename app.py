import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

engine = create_engine('sqlite:///Resources/hawaii.sqlite')

Base = automap_base()
Base.prepare(create_engine('sqlite:///Resources/hawaii.sqlite'), reflect=True)

print(Base.classes.keys())
m = Base.classes.measurement
s = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    return """Welcome to 'A Climate Analysis of Hawaii' API!</br>
    Routes available:</br>
    /api/v1.0/precipitation</br>
    /api/v1.0/stations</br>
    /api/v1.0/tobs</br>
    /api/v1.0/<start></br>
    /api/v1.0/<start>/<end>"""

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(bind=engine)

    results = session.query(m.date, m.prcp).\
                            filter(m.station == s.station).all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(bind=engine)

    results = session.query(s.station, s.name).all()
    
    session.close()

    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(bind=engine)

    results = session.query(m.date, m.tobs).\
                            filter(m.station == s.station).\
                            filter(s.id == 7).\
                            filter(m.date >= year_ago).all()
    
    session.close()

    last_yr_temps = list(np.ravel(results))
    return jsonify(last_yr_temps)

@app.route("/api/v1.0/<start>")
def start():
    return 'Hello'

if __name__ == '__main__':
    app.run(debug=True)
    