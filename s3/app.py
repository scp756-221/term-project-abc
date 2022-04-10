"""
SFU CMPT 756
s3 service  ---  playlist service.
"""

# Standard library modules
import logging
import random
import sys
import time

# Installed packages
from flask import Blueprint
from flask import Flask
from flask import request
from flask import Response

from prometheus_flask_exporter import PrometheusMetrics

import requests

import simplejson as json

# The application
# Integer value 0 <= v < 100, denoting proportion of
# calls to `get_song` to return 500 from
# PERCENT_ERROR = 50

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Playlist process')

db = {
    "name": "http://cmpt756db:30002/api/v1/datastore",
    "endpoint": [
        "read",
        "write",
        "delete",
        "update"
    ]
}
bp = Blueprint('app', __name__)


@bp.route('/health')
@metrics.do_not_track()
def health():
    return Response("", status=200, mimetype="application/json")


@bp.route('/readiness')
@metrics.do_not_track()
def readiness():
    return Response("", status=200, mimetype="application/json")


@bp.route('/<pl_id>', methods=['GET'])
def list_all(pl_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    # list all existing playlists
    payload = {"objtype": "playlist", "objkey": pl_id}
    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    return (response.json())


@bp.route('/write_song_to_playlist/<pl_id>', methods=['PUT'])
def write_song_to_playlist(pl_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    payload = {"objtype": "playlist", "objkey": pl_id}
    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    playlist = response.json()['Items'][0]['Songs']
    try:
        content = request.get_json()
        Songs = content['music_id']
    except Exception:
        return json.dumps({"message": f"error add songs: {Songs}"})
    
    if Songs not in playlist:
        pass
    else:
        return json.dumps({"error": f"song {Songs} is in the" + f"playlist {pl_id}"})
    playlist.append(Songs)
    url = db['name'] + '/' + db['endpoint'][3]
    response = requests.put(
        url,
        params=payload,
        json={"Songs: ": playlist},
        headers={'Authorization': headers['Authorization']})
    return (response.json())


@bp.route('/delete_playlist/<pl_id>', methods=['PUT'])
def delete_playlist(pl_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    try:
        content = request.get_json()
        music_id = content['music_id']
    except Exception:
        return json.dumps({"message": "error reading delete_playlist arguments"})
    playlist = list_all(pl_id)['Items'][0]['Songs']
    if music_id in playlist:
        try:
            playlist.remove(music_id)
        except Exception:
            return json.dumps({"message": f"error delete the music id {music_id}"})
    else:
        return json.dumps({"error": f"music_id {music_id} is not in the playlist"})
    
    url = db['name'] + '/' + db['endpoint'][3]
    response = requests.put(
        url,
        params={"objtype": "playlist", "objkey": pl_id},
        json={"Songs: ":playlist},
        headers={'Authorization': headers['Authorization']})
    return (response.json())

'''
@bp.route('/<pl_id>', methods=['GET'])
def get_songs_from_playlist(pl_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    payload = {"objtype": pl_id, "objkey": ""}
    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    return (response.json())
'''

@bp.route('/', methods=['POST'])
def create_playlist():
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    try:
        content = request.get_json()
        pl_name = content['PlayListName']
        Songs = content['Songs']
    except Exception:
        return json.dumps({"message": "error reading create_playlist arguments"})
    payload = {"objtype": "playlist", "PlayListName": pl_name, "Songs": Songs} # for now only include music_id
    url = db['name'] + '/' + db['endpoint'][1]
    response = requests.post(
        url,
        json=payload,
        headers={'Authorization': headers['Authorization']})
    return (response.json())


@bp.route('/<pl_id>', methods=['DELETE'])
def delete_song_from_playlist(pl_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    
    try:
        content = request.get_json()
        music_id = content['music_id']
    except Exception:
        return json.dumps({"message": "error reading delete_song_from_playlist arguments"})
    
    url = db['name'] + '/' + db['endpoint'][2]
    response = requests.delete(
        url,
        params={"objtype": "playlist", "objkey": pl_id},
        headers={'Authorization': headers['Authorization']})
    return (response.json())

# All database calls will have this prefix.  Prometheus metric
# calls will not---they will have route '/metrics'.  This is
# the conventional organization.
app.register_blueprint(bp, url_prefix='/api/v1/playlist/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("please provide an argument")
        sys.exit(-1)

    p = int(sys.argv[1])
    # Do not set debug=True---that will disable the Prometheus metrics
    app.run(host='0.0.0.0', port=p, threaded=True)
