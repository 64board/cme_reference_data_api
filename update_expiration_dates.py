#!/usr/bin/env python3

import argparse
import sys

from config_db import ConfigDb
from database import Database
from database import DatabaseError
from ref_data import RefData
from ref_data import RefDataError
from config_client import ConfigClient

def main():
    """
    Updates database prices table expiration date field for CME instruments,
    using CME Reference Data API to obtain expiration dates.
    janeiros@mbfcc.com
    2022-11-09
    """

    # Create config file parser.
    parser = argparse.ArgumentParser()
 
    # Add arguments to the parser.
    parser.add_argument("config")
 
    # Parse the arguments.
    args = parser.parse_args()
 
    config_file = args.config

    try:
        instruments = []

        c = ConfigDb(config_file)

        with Database(c) as db:
    
            print('Connecting to: {} ...'.format(c.host))

            sql = """
            SELECT s.mbf_symbol, s.mdp3_symbol, p.contract, p.expires
            FROM pltracker.cme_symbols AS s
            INNER JOIN pltracker.prices AS p ON s.mbf_symbol = p.symbol
            WHERE p.expires IS NULL AND s.mdp3_symbol IS NOT NULL;
            """

            prices = db.query(sql)
    
            if len(prices) > 0:
                print('Instruments with null expiration dates found.')

                for (symbol_mbf, mdp3_symbol, contract, expires) in prices:
                    print('{}|{}|{} -> {}'.format(symbol_mbf, mdp3_symbol, contract, expires))
                    instruments.append({'symbol_mbf' : symbol_mbf, 'mdp3_symbol' : mdp3_symbol, 'contract' : contract, 'expires' : expires})
            else:
                print('All instruments have expiration dates.')
                sys.exit(1)

            print('Updating instruments expiration dates ...')
            c = ConfigClient(config_file)
            rd = RefData(c)
            
            for i in instruments:
                print('Searching {} ...'.format(i['symbol_mbf']+i['contract']))
                
                date = rd.find_expire_date(i['mdp3_symbol'], i['contract'])

                if date != None: 
                    print('Updating {} with {} ...'.format(i['symbol_mbf']+i['contract'], date))
                    db.execute('UPDATE prices SET expires = %s WHERE symbol = %s AND contract = %s', (date, i['symbol_mbf'], i['contract']))
                else:
                    print('No expiration date found for {} ...'.format(i['symbol_mbf']+i['contract'], date))

    except (ValueError, DatabaseError, RefDataError) as e:
        print(e)

if __name__ == '__main__':
    main()
    
