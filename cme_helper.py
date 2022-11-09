#!/usr/bin/env python3

class CMEHelper:

    """
    Static class to help with CME features.
    """

    @staticmethod
    def convert_to_cme_instrument(instrument):
        """
        Helper function to convert an instrument in the format HETX22 to HET2.
        """
        symbol_month = instrument[0:len(instrument) - 2]
        year = instrument[-1:]
        
        return symbol_month + year

    @staticmethod
    def convert_to_iso_date(self, date):
        """
        Helper function to convert a mm/dd/yyyy date to an ISO format date yyyy-mm-dd.
        """
        (month, day, year) = date.split('/')
        return '{}-{}-{}'.format(year, month, day)
