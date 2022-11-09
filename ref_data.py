#!/usr/bin/env python3

import requests
import sys
from config_client import ConfigClient
from cme_helper import CMEHelper

class RefDataError(Exception):
    """
    Custom RefData Exception.
    """
    def __init__(self, msg, *args):
        super().__init__(args)
        self.msg = msg

    def __str__(self):
        return self.msg

class RefData:
    """
    Creates a class to query CME Reference Data API.
    Uses a ConfigClient class.
    """

    def __init__(self, config):

        try:

            self._url_query = config.url_query

            payload = {'client_id': config.client_id, 'client_secret' : config.client_secret, 'grant_type': config.grant_type}

            r = requests.post(config.url_oauth, data=payload)

            if r.status_code == 404:
                raise RefDataError('RefData: HTTP Error 404.', '')

            json = r.json()

            self._access_token = json['access_token']

        except ValueError as e:
            raise RefDataError('RefData: Error decoding JSON.', e)

    def find_expire_date(self, instrument):
        """
        Returns a date string for a given instrument, if the instrument
        doesn't exist returns None.
        """
        cme_instrument = CMEHelper.convert_to_cme_instrument(instrument)
        
        query = '{}/v2/instruments?globexSymbol={}'.format(self._url_query, cme_instrument)
    
        auth_header = {'Authorization' :  'Bearer {}'.format(self._access_token)}

        r = requests.get(query, headers=auth_header)

        try: 
            response = r.json()
            date = response['_embedded']['instruments'][0]['lastTradeDate']
        except KeyError as e:
            date = None

        return date

def main():

    try:
        c = ConfigClient('config_testing.ini')
        rd = RefData(c)

        for i in ('BTCF23', 'BTCG23', 'BTCX22', 'BTCZ22', 'CLTQ23', 'CLTZ23'):
            ed = rd.find_expire_date(i)
            print('{} -> {}'.format(i, ed))
    except RefDataError as e:
        print(e)

if __name__ == '__main__':
    main()