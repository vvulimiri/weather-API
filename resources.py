from flask_restful import Resource, reqparse
from flask import request,jsonify
from models import WeatherData, WeatherAnalysis, db
from datetime import datetime

class WeatherResource(Resource):
    def get(self):
        # Parse query arguments
        stationId = request.args.get('stationId', type=int, default=None)
        date = request.args.get('date', default=None, type=str)
        page = request.args.get('page', type=int, default=1)
        # Base query
        query = WeatherData.query

        # Apply filters
        if stationId:
            query = query.filter(WeatherData.stationId == stationId)
        if date:
             # Convert the string into a datetime object
            date_obj = datetime.strptime(date, "%Y%m%d")  # Adjust the format as needed
        # Format it to 'YYYYMMDD'
            formatted_date = date_obj.strftime("%Y%m%d")
            query = query.filter(WeatherData.date == formatted_date)
           
        # Pagination
        page = page
        per_page = 10
        print(query)

        weather_data = query.paginate(page=page, per_page=per_page, error_out=False)
        # Serialize results manuall
        # y
        data = []
        for record in weather_data.items:
            data.append({
                'id': record.id,
                'stationId': record.stationId,
                'date': record.date,
                'maxTemperature': record.maxTemperature,
                'minTemperature': record.minTemperature,
                'precipitation': record.precipitation
            })

        return jsonify({
            'data': data,
            'page': weather_data.page,
            'total_pages': weather_data.pages,
            'total_count': weather_data.total
        })


class WeatherStatsResource(Resource):
    def get(self):
        stationId = request.args.get('stationId', type=int, default=None)
        year = request.args.get('year', default=None, type=str)

        # Base query for aggregation
        query = WeatherAnalysis.query

        # Apply filters
        if stationId:
            query = query.filter(WeatherAnalysis.stationId == stationId)
        if year:
            query = query.filter(WeatherAnalysis.year == year)

        # Execute query and return the result
        results = query.all()
        data = []
        for result in results:
            data.append({
                'stationId': result.stationId,
                'year': result.year,
                'avgMaxTemperature': result.avgMaxTemperature,
                'avgMinTemperature': result.avgMinTemperature,
                'totalPrecipitation': result.totalPrecipitation
            })

        return jsonify(data)
