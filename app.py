# -*- coding: utf-8 -*-
import requests
from flask import Flask, request, jsonify, make_response
from flask_caching import Cache
from config import redis_config, logger
from apputility import get_temp, get_wind

app = Flask (__name__)
app.config.from_pyfile ('config.py')

redis_config = redis_config
cache = Cache (app, config=redis_config)


@cache.memoize (timeout=redis_config['CACHE_DEFAULT_TIMEOUT'])
def get_data_from_nws(url):
    response = requests.request ("GET", url, headers={}, data={})

    if response:
        data = response.text.strip ().split ('\n')

        if len (data) >= 1 and data[0]:
            raw_data_first_line = data[0].split (' ')
            date_last_observed = raw_data_first_line[0] if len (raw_data_first_line) >= 1 and raw_data_first_line[0] else None
            time_last_observed = raw_data_first_line[1] if len (raw_data_first_line) >= 2 and raw_data_first_line[1] else None
            last_observation = f'{date_last_observed} at {time_last_observed} GMT'

        else:
            return {'error': 'data not exist or can not be retrieved.'}, 400

        if len (data) >= 2 and data[1]:
            raw_data_second_line = data[1].split (' ')
            station = raw_data_second_line[0]
            current_temperature = None
            current_wind = None
            invalid = True
            for idx, elem in enumerate (raw_data_second_line[1:]):
                if elem.endswith ('KT') and '/' not in elem:
                    current_wind = get_wind (first_elem=elem)
                if '/' in elem and elem.count ('/') == 1 and invalid:
                    current_temperature = get_temp (first_elem=elem)
                    if not current_temperature == "Unknown":
                        invalid = False

        else:
            return {'error': 'data not exist or can not be retrieved.'}, 401

    else:
        return {'error': 'data retrieval error.'}, 402

    return {
               'station': station,
               'last_observation': last_observation,
               'temperature': current_temperature,
               'wind': current_wind
               }, 200


@app.route ('/metar/ping/', methods=['GET'])  # api 1 from SRS
def ping():
    return jsonify ({'data': 'pong'})


@app.route ('/clear_cache/', methods=['GET'])  # clear all cache
def clear_cache():
    cache.init_app (app, config=redis_config)
    with app.app_context ():
        cache.clear ()
    return jsonify ({'msg': 'Redis cache cleared'}), 200


@app.route ('/metar/info', methods=['GET'])  # api 2 from SRS
def meter_info():
    global nws_data

    scode = request.args.get ('scode')
    nocache = request.args.get ('nocache')

    if scode is None:
        logger.error ('ERROR 400: Missing scode in request')
        return jsonify ({'error': 'Missing scode in request'}), 400

    if nocache is None:
        nocache = 0
    else:
        nocache = int (request.args.get ('nocache'))

    api_url = app.config['NWS_URL'] + scode + app.config['NWS_RESPONSE_FILE_TYPE']

    if nocache:  # update redis
        cache.delete_memoized (get_data_from_nws, api_url)
        nws_data = get_data_from_nws (url=api_url)
    else:  # redis cache
        nws_data = get_data_from_nws (url=api_url)

    return jsonify ({'data': nws_data})


if __name__ == "__main__":
    app.run (host="0.0.0.0", debug=True, port=8080)
