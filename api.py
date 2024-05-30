from flask import Flask, request, jsonify, render_template, Blueprint, send_from_directory
from flask_cors import CORS
from flask_caching import Cache
import rozklad_jazdy
import os

app = Flask(__name__)
CORS(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

os.environ['TZ'] = 'CET-1CEST,M3.5.0,M10.5.0/3'


@app.route('/get_bus_stop_data', methods=['GET'])
@cache.cached(key_prefix=lambda: request.args.get('number_of_stop'), timeout=20)
def get_bus_stop_data():
    number_of_stop = request.args.get('number_of_stop')
    table_data = rozklad_jazdy.get_table_data(number_of_stop)
    return jsonify(table_data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rozklad')
def rozklad():
    id_param = request.args.get('id')
    return render_template('rozklad.html', id=id_param)

@app.route('/manifest.json')
def manifest():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'manifest.json')

@app.route('/export.geojson')
def geojson():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'export.geojson')

@app.route('/stops.txt')
def stopscsv():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'stops.txt')

if __name__ == '__main__':
    #app.run(port=5001, host='0.0.0.0', ssl_context='adhoc', debug=True)
    #or use 
    app.run(port=5001, host='0.0.0.0', debug=True)