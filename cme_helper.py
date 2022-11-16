#!/usr/bin/env python3

import re
from datetime import date

class CMEHelper:

    """
    Static class to help with CME features.
    """

    @staticmethod
    def convert_to_cme_instrument(symbol, contract):
        """
        Helper function to convert a symbol and contract with format HETX22
        to HET2.
        """
        if len(contract) > 6:
            (contract_month, contract_year, strike, call_put) = CMEHelper.extract_contract(symbol, contract)
        else:
            strike = call_put = ''
            contract_month = contract[0]
            contract_year = contract[1:3]

        # Use 2 digits for years >= 30.
        #if int(contract_year) >= 30:
        #    year = contract_year
        #else:
            # Only the last digit.
        #    year = contract_year[-1]

        year = CMEHelper.to_cme_year(contract_year)  # type: ignore

        return '{}{}{} {}{}'.format(symbol, contract_month, year, call_put, strike).strip()

    @staticmethod
    def convert_to_iso_date(date):
        """
        Helper function to convert a mm/dd/yyyy date to an ISO format date yyyy-mm-dd.
        """
        (month, day, year) = date.split('/')
        return '{}-{}-{}'.format(year, month, day)

    @staticmethod
    def is_contract(contract):
        p = re.compile(r'^[FGHJKMNQUVXZ]\d{2}(\s\d{5}[CP])?$')
        if p.match(contract):
            return True
        else:
            return False

    @staticmethod
    def extract_contract(symbol, contract):
        month = year = strike = put_call = None

        m = re.search(r'([FGHJKMNQUVXZ])(\d{2})(\s(\d{5})([CP]))?', contract)

        if m != None:
            month = m.group(1)
            year = m.group(2)
            strike = m.group(4)
            put_call = m.group(5)

            if strike != None:  # Options
                if symbol in ('ADU', 'CAU', 'EUU', 'GBU', 'JPU'):
                    # Truncate to 4 digits.
                    strike = strike[:-1]
                elif strike[0] == '0':
                    strike = strike[1:]

        return (month, year, strike, put_call)

    @staticmethod
    def to_cme_year(year: str) -> str:
        
        current_year = int(date.today().strftime('%y'))
        
        current_decade = current_year // 10 * 10
        next_decade = current_decade + 10

        contract_year = int(year)

        if contract_year >= next_decade:
            # Return year as 2 digits number.
            cme_year = contract_year
        else:
            # One digit year.
            cme_year = contract_year % 10

        return str(cme_year)

def main():

    print(CMEHelper.to_cme_year('23'))
    print(CMEHelper.to_cme_year('29'))
    print(CMEHelper.to_cme_year('30'))
    print(CMEHelper.to_cme_year('31'))
    print(CMEHelper.to_cme_year('43'))

    for c in ('N22', 'Q29', 'F30', 'G31'):
        print(CMEHelper.convert_to_cme_instrument('BTC', c))

    """
    for c in ('F23 09500C', 'F30 10000C', 'F23 20000C'):
        print(CMEHelper.convert_to_cme_instrument('LNE', c))

    for c in ('F23 09500C', 'F30 10000C', 'F23 20000C'):
        print(CMEHelper.convert_to_cme_instrument('EUU', c))
    
    #for c in ('N22 05460P', 'N22', 'F2'):
    #    print(f'{c:15}>{CMEHelper.is_contract(c)}<')

    #    (month, year, strike, put_call) = CMEHelper.extract_contract(c)
    #    print(f'{c:15}{month} {year} {strike} {put_call}')
    """

if __name__ == '__main__':
    main()    
