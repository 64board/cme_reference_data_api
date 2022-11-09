#!/usr/bin/env python3

import configparser

class ConfigClient:
    """Simple class wrapper around ConfigParser to read a specific section of a .INI file."""

    def __init__(self, file_name):
        self.config = configparser.ConfigParser()
        self.config.read(file_name)

        if not self.config.has_section('CLIENT'):
            raise ValueError('No [CLIENT] section found!')

        self._client_id = self.config.get('CLIENT', 'client_id')
        self._client_secret = self.config.get('CLIENT', 'client_secret')
        self._grant_type = self.config.get('CLIENT', 'grant_type')
        self._url_oauth = self.config.get('CLIENT', 'url_oauth')
        self._url_query = self.config.get('CLIENT', 'url_query')

    @property
    def client_id(self):
        return self._client_id

    @property
    def client_secret(self):
        return self._client_secret

    @property
    def grant_type(self):
        return self._grant_type
    
    @property
    def url_oauth(self):
        return self._url_oauth

    @property
    def url_query(self):
        return self._url_query

def main():
    try:
        c = ConfigClient('config_testing.ini')
        print(c.client_id)
    except ValueError as e:
        print(e)

if __name__ == '__main__':
    main()
    
