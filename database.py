#!/usr/bin/env python3

import mysql.connector
from config_db import ConfigDb

class DatabaseError(Exception):
    """
    Custom Database Exception.
    """
    def __init__(self, msg, *args):
        super().__init__(args)
        self.msg = msg

    def __str__(self):
        return self.msg

class Database:
    """
    Handle mySQL database connections.
    Requires a ConfigDB instance.
    """

    def __init__(self, config):

        try:

            self._connection = mysql.connector.connect(
                user=config.user,
                password=config.password,
                host=config.host,
                database=config.database)

        except (mysql.connector.Error) as e:
            raise DatabaseError(e.msg, e.errno)

        self._cursor = self._connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._connection

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

def main():

    try:
        c = ConfigDb('config_testing.ini')

        with Database(c) as db:
            sql = """
            SELECT s.mbf_symbol, s.cme_symbol, p.contract, p.expires
            FROM pltracker.cme_symbols AS s
            INNER JOIN pltracker.prices AS p ON s.mbf_symbol = p.symbol
            WHERE expires IS NULL;
            """
            prices = db.query(sql)
            for (symbol_mbf, symbol_cme, contract, expires) in prices:
                print('{}|{}|{} -> {}'.format(symbol_mbf, symbol_mbf, contract, expires))

    except (ValueError, DatabaseError) as e:
        print(e)

if __name__ == '__main__':
    main()
    
