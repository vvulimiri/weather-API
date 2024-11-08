from flask import Flask
from flask_restful import Api
from models import db
from resources import WeatherResource, WeatherStatsResource
from flask_swagger_ui import get_swaggerui_blueprint
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Set up Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swagger_ui = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Weather API"})
app.register_blueprint(swagger_ui, url_prefix=SWAGGER_URL)

# Set up API
api = Api(app)
api.add_resource(WeatherResource, '/api/weather')
api.add_resource(WeatherStatsResource, '/api/weather/stats')

if __name__ == '__main__':
    app.run(debug=True)
