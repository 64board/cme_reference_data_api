#!/usr/bin/env python3

import configparser

class ConfigDb:
    """Simple class wrapper around ConfigParser to read a specific section of a .INI file."""

    def __init__(self, file_name):
        self.config = configparser.ConfigParser()
        self.config.read(file_name)

        if not self.config.has_section('MYSQL'):
            raise ValueError('No [MYSQL] section found!')

        self._user = self.config.get('MYSQL', 'user')
        self._password = self.config.get('MYSQL', 'password')
        self._host = self.config.get('MYSQL', 'host')
        self._database = self.config.get('MYSQL', 'database')
        self._port = self.config.get('MYSQL', 'port')

    @property
    def user(self):
        return self._user

    @property
    def password(self):
        return self._password

    @property
    def host(self):
        return self._host
    
    @property
    def database(self):
        return self._database

    @property
    def port(self):
        return self._port

def main():
    try:
        c = ConfigDb('config_db.ini')
        print(c.database)
    except ValueError as e:
        print(e)

if __name__ == '__main__':
    main()
    
