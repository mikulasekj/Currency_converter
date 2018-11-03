
"""This module convert given amount of input currency into output currencies.

3-letter string (code form of currency) or the symbol could be given
as input or output currency. If the symbol is given as an input or output
than both are converted into code form. This conversion is performed using
code-symbol dictionary. The amount type is not checked in this class because
it is checked directly in currency_convertor.py or currency_converter_api.py via
argparse resp reqparse module. The amount could inserted as negative number and
and in such a case the results are also negative.
Currencies are converted using currency-rate dictionary for given base currency.
Currency rate dictionary is obtained from fixer.io api and stored as JSON file.
Currency rates on fixer.io site is updated ones per hour, so if the latest stored
currency-rate dictionary is not actaul than the new request is send. In other case
the stored one is used. Also in case when request failed the latest stored 
currency-rates dictionary is used.
"""
import time
from decimal import Decimal
import requests
import simplejson as json

class WrongInputCurrencyError(Exception):
    """ Raised when input currency string is not in list of currencies
        code either in list of symbol currency
    """
    pass        

class WrongOutputCurrencyError(Exception):
    """ Raised when output currency string is not in list of currencies
        code either in list of symbol currency
    """
    pass

class FixerApiIsNotAvailableError(Exception):
    """ Rasied when response status is not 200"""
    pass
        
    
class Convertor:
    """The class containg all neccessary staff for currency converting"""
    
    def __init__(self):
        """During initialization are setted all class atributes.
            The code-symbol dictionary is created from stored JSON file.
            The symbol-code dictionary is created from code-symbol dictionary
            to enable converting szmbols into codes.
            Latest code-rates file is loaded and the timestamp is extracted.
            If the difference between lates stored timestamp and current
            timestamp is bigger than 1 hour (update peride on fixer.io) than 
            actual code-rate JSON is downloaded from fixer.io and loaded again.
            In case when the stored file is actual or the request fail the existing
            code-rate dict is used.
        """

        self.base_currency = 'EUR'
        self.not_actual_rates_warning = None

        with open('code_symbol.json', 'r', encoding="utf8") as file_in:
            self.code_symbol_dict = json.load(file_in)

        self.symbol_code_dict = {key:value for value, key in self.code_symbol_dict.items()}
        
        with open('fixer_rates.json', 'r', encoding="utf8") as file_in:
            rates_json = json.load(file_in)
        
        latest_updating_timestamp = rates_json['timestamp']
        curr_timestamp = time.time()        
        time_diff_timestamp = curr_timestamp-latest_updating_timestamp
        update_time = 5
        
        if time_diff_timestamp > update_time:
            if self._get_actaul_rates():
                with open('fixer_rates.json', 'r', encoding="utf8") as file_in:
                    rates_json = json.load(file_in)

        self.rates_dict = rates_json['rates']
            
    def _create_and_check_final_input_curr(self, given_input_currency):
        """3-letter string (code form of currency) or the symbol is given 
           as a given_input_currency. If the input currency is symbol, than it is converted
           into the exact corresponding code - that is differrent
           from output currency - see below.
           Check if the input currency is valid code, if not check if it is a valid symbol.
           If yes, convert it to the code. If neither one of conditions above are satisfied,
           than raise the WrongInputCurrencyError
        """                
        if given_input_currency in self.code_symbol_dict.keys():
            final_input_currency = given_input_currency
        
        elif given_input_currency in self.symbol_code_dict.keys():
            final_input_currency = self.symbol_code_dict[given_input_currency]
            
        else:
            raise WrongInputCurrencyError('The input currency is not supported.')

        return final_input_currency       
        

    def _create_and_check_final_output_curr(self, given_output_currency):
        """3-letter string (code form of currency) or the symbol is given 
           as a given_output_currency.
           Check if the output currency is valid code, if not check if it is a valid symbol
           and convert it to all codes contanaining the input currency smybol - including the input
           currency if its symbol contains given output symbol.
           If the input is not entered than creates list of codes of all available currencies.
           Finally compare the list of output currencies with currencies provided by fixier rates
           and reduce the list of output currencies only on common currencies.
           If neither one of conditions above are satisfied,
           than raise the WrongInputCurrencyError
        """
        semifinal_output_curr_list = []
        if given_output_currency in self.code_symbol_dict.keys():
            semifinal_output_curr_list = [given_output_currency]

        elif given_output_currency in self.symbol_code_dict.keys():
            for curr_symbol in self.symbol_code_dict.keys():
                if given_output_currency in curr_symbol:
                    semifinal_output_curr_list.append(self.symbol_code_dict[curr_symbol])

        elif given_output_currency is None:
            semifinal_output_curr_list = self.code_symbol_dict.keys()
        else:
            raise WrongOutputCurrencyError('The output currency is not supported.')
        
        final_output_curr_list = list(set(semifinal_output_curr_list)&set(self.rates_dict.keys()))
        if not final_output_curr_list:
            raise WrongOutputCurrencyError('The output currency is not supported.')
        
        return final_output_curr_list
        
    def _get_actaul_rates(self):
        """Send a request on fixer api. If the status code of a response is 200
        than is verified if the key 'success' in response JSON file is 'true'. 
        If yes the response JSON file is stored as latest code-rates dictionary.
        Otherwise the FixerApiIsNotAvailableError or ConnectionError is raised. 
        The exceprions are handeld and program contue with non-actualized code-rates dictionary
        """

        base_url = 'http://data.fixer.io/api/latest'
        access_key = 'access_key=1f45f76495a5436a9a6fabca5884f2a2'
        rate_url = (base_url+'?'+access_key)   
    
        try:
            fixer_rates_response = requests.get(rate_url)
            
            if fixer_rates_response.status_code == 200:
                fixer_rates_json = fixer_rates_response.json()
                if fixer_rates_json['success']:
                    with open('fixer_rates.json', 'w', encoding="utf8") as file_out:
                        json.dump(fixer_rates_json, file_out, indent=4)
                    return True
            raise FixerApiIsNotAvailableError()
        except (FixerApiIsNotAvailableError, requests.exceptions.ConnectionError):
            self.not_actual_rates_warning = ('Fixer api failed - '
                                             'not latest rates may be used for conversion')
            
            

    def _convert_currency(self, input_curr, output_curr, amount):
        """Covnert input currency to output currency using code-rate dictionary
           and base_currency EUR. The inputed float types are converted int decimals
           Amount type could be given with minus sign - results are than negative.
        """
        amount_in_decimal = Decimal(str(amount))

        if input_curr == output_curr:
            converted_currency = amount_in_decimal

        elif input_curr == self.base_currency:
            converted_currency = amount_in_decimal*Decimal(str(self.rates_dict[output_curr]))

        elif output_curr == self.base_currency:
            converted_currency = amount_in_decimal/Decimal(str(self.rates_dict[input_curr]))

        else:
            base_amount = amount_in_decimal/Decimal(str(self.rates_dict[input_curr]))
            converted_currency = base_amount*Decimal(str(self.rates_dict[output_curr]))

        return converted_currency
            
          
    def to_convert(self, input_currency, amount, output_currency=None):
        """Use "private" functions _create_and_check_inputs(),_create_and_check_outputs()
           and _convert_currency() to performe all the neccesary stuff to convert given inputs.
        """
        
        final_input_currency = self._create_and_check_final_input_curr(input_currency)
        final_output_currency_list = self._create_and_check_final_output_curr(output_currency)
        
        output_dict = {}  
        
        for curr in final_output_currency_list:
            
            converted_value = self._convert_currency(final_input_currency, curr, amount) 
            converted_value = round(converted_value, 2)
            output_dict.update({curr:converted_value})

        if self.not_actual_rates_warning is None:
            result_dict = {
                "input":{"amount":amount, "currency":final_input_currency},
                "output":output_dict
                }

        else:
            result_dict = {
                "WARNING":self.not_actual_rates_warning,
                "input":{"amount":amount, "currency":final_input_currency},
                "output":output_dict
                }
        result_json = json.dumps(result_dict, indent=4)

        return result_json

