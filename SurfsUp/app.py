import numpy as np
#import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


engine = create_engine("sqlite:///../Resources/hawaii.sqlite", connect_args={'check_same_thread': False})


Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)
app = Flask(__name__)

startDate = (session.query(Measurement.date).order_by(Measurement.date.desc()).first())
startDate = np.ravel(startDate)[0]
endDate = dt.datetime.strptime(startDate, '%Y-%m-%d') - dt.timedelta(days=1 * 365)
endDate = (endDate.strftime('%Y-%m-%d'))

@app.route("/")
def home():
    return (f"Test<br/>")


@app.route('/api/v1.0/precipitation')
def precipitation():
    prcp_results = (session.query(Measurement.date, Measurement.prcp)
                    .filter(Measurement.date > endDate)
                    .order_by(Measurement.date.asc())
                    .all())
    test = {}
    test_list = ['Date','Precipitation']
    for row in prcp_results:
        test.update({row.date: row.prcp})
        test_list.append(test)

    return jsonify(test_list)

@app.route('/api/v1.0/stations')
def stations():
    station_results = (session.query(Station.name).all())
    return jsonify(station_results)

@app.route('/api/v1.0/tobs')
def tobs():
    tobs_results = (session.query(Measurement.date, Measurement.tobs)
                    .filter(Measurement.date > endDate)
                    .order_by(Measurement.date.asc())
                    .all())
    tobs_dict = {}
    tobs_list = ['Date', 'Tobs']
    for row in tobs_results:
        tobs_dict.update({row.date: row.tobs})
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)


if __name__ == "__main__":
    app.run(debug=True)


