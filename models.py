from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class WeatherData(db.Model):
    __tablename__ = 'weather_data'
    id = db.Column(db.Integer, primary_key=True)
    stationId = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(8), nullable=False)
    maxTemperature = db.Column(db.Integer, nullable=True)
    minTemperature = db.Column(db.Integer, nullable=True)
    precipitation = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<WeatherData {self.stationId} {self.date}>'

class WeatherAnalysis(db.Model):
    __tablename__ = 'weather_analysis'
    id = db.Column(db.Integer, primary_key=True)
    stationId = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    avgMaxTemperature = db.Column(db.Float)
    avgMinTemperature = db.Column(db.Float)
    totalPrecipitation = db.Column(db.Float)

    def __repr__(self):
        return f'<WeatherAnalysis {self.stationId} {self.year}>'
