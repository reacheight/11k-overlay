from steam.client import SteamClient
from steam.utils.proto import proto_to_dict
from dota2.client import Dota2Client

import logging
from os import environ

logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level='INFO')
logger = logging.getLogger(__name__)


class DotaProxy:
    def __init__(self):
        self.steam = steam = SteamClient()
        self.dota = dota = Dota2Client(self.steam)
        steam.connect()

        @steam.on('connected')
        def log_in():
            logger.info('Logging in')
            steam.login(environ['STEAM_LOGIN'], environ['STEAM_PASSWORD'])

        @steam.on('logged_on')
        def start_dota():
            logger.info('Logged on, launching dota client')
            dota.launch()

        @dota.on('ready')
        def do_dota_stuff():
            logger.info('Dota is ready')

    def get_match_details(self, match_id):
        if not self.dota.ready:
            return

        job_id = self.dota.request_match_details(int(match_id))
        match_details = self.dota.wait_msg(job_id)
        return proto_to_dict(match_details)
