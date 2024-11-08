import unittest
from unittest.mock import patch
from app import app, db
from models import WeatherData, WeatherAnalysis
from datetime import datetime

class WeatherApiTestCase(unittest.TestCase):
    def setUp(self):
        
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        # Mock data
        weather = WeatherData(stationId=999, date="20240101", maxTemperature=235, minTemperature=115, precipitation=65)
        a = WeatherAnalysis(stationId=999,year=2024,avgMaxTemperature=99, avgMinTemperature=55, totalPrecipitation=100)
        db.session.add(weather)
        db.session.add(a)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_weather(self):
        response = self.app.get('/api/weather?page=1&per_page=1')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn('data', data)
        self.assertEqual(len(data['data']), 1)

    def test_get_weather_filtered_by_station(self):
        response = self.app.get('/api/weather?stationId=999')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['stationId'], 999)

    def test_get_stats(self):
        response = self.app.get('/api/weather/stats')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data), 1)  # 2 stations
        self.assertIn('avgMaxTemperature', data[0])
        self.assertIn('totalPrecipitation', data[0])

if __name__ == '__main__':
    unittest.main()
