import numpy as np
#import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.

    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d

    Returns:
        TMIN, TAVE, and TMAX
    """

    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)). \
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()


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
    return (f"<h1>Weather Analysis</h1><br/>"
            f"<h2>Links</h2><br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/datesearch/*your start date here */*your end date here*")


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

@app.route('/api/v1.0/datesearch/<startDate>/<endDate>')
def start(startDate,endDate):
    range_results = calc_temps(startDate,endDate)
    return jsonify(range_results)




if __name__ == "__main__":
    app.run(debug=True)


