from gevent import monkey
monkey.patch_all()

from steam.enums import EResult
from flask import Flask, jsonify
from dota_proxy import DotaProxy

app = Flask(__name__)
client = DotaProxy()


@app.route('/matches/<int:match_id>', methods=['GET'])
def get_match_details(match_id):
    match_details = client.get_match_details(match_id)

    if not match_details:
        return 'Dota client is not yet ready', 400

    if match_details['result'] != EResult.OK:
        return f"Can't find match {match_id}", 400

    return match_details


@app.route('/client/status', methods=['GET'])
def get_dota_client_status():
    return jsonify(client.dota.ready)
