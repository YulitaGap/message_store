from flask import Flask, render_template
from flask_restful import Resource, Api
from api_endpoints import *


app = Flask(__name__, static_url_path='/static')
api = Api(app, prefix="/api")
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def index():
    return render_template("index.html")


for endpoint in ENDPOINTS_LIST:
    api.add_resource(endpoint, endpoint.ROUTE)

if __name__ == '__main__':
    app.run(debug=True)
