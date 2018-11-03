# from forex_python.converter import CurrencyRates
# from forex_python.converter import CurrencyCodes
import requests
import datetime
import time
import dateutil.relativedelta
import pdb
#import timeit

from decimal import Decimal

import simplejson as json

class WrongInputCurrencyError(Exception):
    """ Raised when input currency string is not in list of currencies code either in list of symbol currency"""
    pass        

class WrongOutputCurrencyError(Exception):
    """ Raised when output currency string is not in list of currencies code either in list of symbol currency"""
    pass

class FixerApiIsNotAvailableError(Exception):
    """ Rasied when response status is not 200"""
    pass
        
    
class Convertor:

    #initialize the object of convertor class with given atributes
    def __init__(self):

        self.base_currency='EUR'

        #self._get_actaul_rates()

        #t1=timeit.default_timer()
        # load the json file with currencies codes and symbols
        #vyjimky na otevirani souboru
        with open('code_symbol.json',encoding="utf8") as f:
            self.code_symbol_dict = json.load(f)

        self.symbol_code_dict={key:value for value,key in self.code_symbol_dict.items()}
        
        with open('fixer_rates.json','r',encoding="utf8") as f:
            rates_json = json.load(f)
        
        latest_updating_timestamp=rates_json['timestamp']
        curr_timestamp=time.time()        
        time_diff_timestamp=curr_timestamp-latest_updating_timestamp
        actualized=24000
        
        if time_diff_timestamp > actualized:
            #pdb.set_trace()
            if self._get_actaul_rates():
                with open('fixer_rates.json','r',encoding="utf8") as f:
                    rates_json = json.load(f)
                #print('success'+ str(rates_json['success']))

        self.rates_dict=rates_json['rates']
            

        print(rates_json['timestamp'])
        print(curr_timestamp)
        print(time_diff_timestamp)

        #create dictionary with key as a symbol and code as a value
        self.symbol_code_dict={key:value for value,key in self.code_symbol_dict.items()}

        #t2=timeit.default_timer()
        #print(t2-t1)

    
    def _create_and_check_final_input_curr(self,given_input_currency):
        """Check if the input currency is valid code, if not check if it is a valid symbol
           and convert it to code if yes. If neither one of conditions above are satisfied,
           than raise the WrongInputCurrencyError
        """
        #tr:                
        if given_input_currency in self.code_symbol_dict.keys():
            final_input_currency=given_input_currency
        
        elif given_input_currency in self.symbol_code_dict.keys():
            final_input_currency=self.symbol_code_dict[given_input_currency]
            
        else:
            raise WrongInputCurrencyError('The input currency is not supported.')

        return final_input_currency       
        

    def _create_and_check_final_output_curr(self,given_output_currency):
        """Check if the output currency is valid code, if not check if it is a valid symbol
           and convert it to codes which symbols contanis the input currency smybol.
           If the input is not entered than creates list of codes of all available currencies.
           Finally compare the list of output currencies with currencies provided by fixier rates
           and reduce the list of output currencies only on common currencies.
           If neither one of conditions above are satisfied,
           than raise the WrongInputCurrencyError
        """
        semifinal_output_curr_list=[]
        if given_output_currency in self.code_symbol_dict.keys():
            semifinal_output_curr_list=[given_output_currency]

        elif given_output_currency in self.symbol_code_dict.keys():
            for curr_symbol in self.symbol_code_dict.keys():
                if given_output_currency in curr_symbol:
                    semifinal_output_curr_list.append(self.symbol_code_dict[curr_symbol])

        elif given_output_currency is None:
            semifinal_output_curr_list=self.code_symbol_dict.keys()
        else:
            raise WrongOutputCurrencyError('The output currency is not supported.')
        
        final_output_curr_list=list(set(semifinal_output_curr_list)&set(self.rates_dict.keys()))
        if not final_output_curr_list:
            raise WrongOutputCurrencyError('The output currency is not supported.')
        
        return final_output_curr_list
        

    #DOPLNIT VYJÍMKY - co kdz6 dojdou pokusz  A OTESTOVAT!!!!!!!!
    #KAM UKLÁDAT???????????
    def _get_actaul_rates(self):
        """rates are actualized 1/hour"""

        base_url='http://data.fixer.io/api/latest'
        access_key='access_key=1f45f76495a5436a9a6fabca5884f2a2'
        rate_url=(base_url+'?'+access_key)   
    
        try:
            #self.forex_rates=CurrencyRates().get_rates(self.base_currency)
            fixer_rates_response = requests.get(rate_url)
            print(fixer_rates_response.status_code)
    
            
            if fixer_rates_response.status_code==200:
                fixer_rates_json=fixer_rates_response.json()
                if fixer_rates_json['success']:
            # doplnit kdyz vycerpam pokusy
                    with open('fixer_rates.json','w',encoding="utf8") as f:
                        json.dump(fixer_rates_json,f,indent=4)
                    return True
                else:
                    raise FixerApiIsNotAvailableError()
            else:
                raise FixerApiIsNotAvailableError()
            return False
        except (FixerApiIsNotAvailableError,requests.exceptions.ConnectionError):
            print('Fixer api failed - not latest rates may be used for conversion')

            
        

        


    def _convert_currency(self,input_curr,output_curr,amount):
        """Covnert input currency to output currency using base_currency EUR"""

        amount_in_decimal=Decimal(str(amount))

        if input_curr==output_curr:
            converted_currency=amount_in_decimal

        elif input_curr==self.base_currency:
            converted_currency=amount_in_decimal*Decimal(str(self.rates_dict[output_curr]))

        elif output_curr==self.base_currency:
            converted_currency=amount_in_decimal/Decimal(str(self.rates_dict[input_curr]))

        else:
            base_amount=amount_in_decimal/Decimal(str(self.rates_dict[input_curr]))
            converted_currency=base_amount*Decimal(str(self.rates_dict[output_curr]))

        return converted_currency
            
          
    def to_convert(self,input_currency,amount,output_currency=None):
        """Use "private" functions _get_actual_rates(),_create_and_check_inputs(), _create_and_check_outputs()
           and _convert_currency() to performe all the neccesary stuff to convert given inputs. 
           If there is no output currency the input currency is converted into all possilbew currencies
        """
        
        #self._get_actaul_rates()
        
        #t1=timeit.default_timer()
        
        final_input_currency=self._create_and_check_final_input_curr(input_currency)
        final_output_currency_list=self._create_and_check_final_output_curr(output_currency)
        
        output_dict={}  
        #t2=timeit.default_timer()

        # if the output value is not given the whole known(by forex) currencies are outputed
        
        for curr in final_output_currency_list:
            
            converted_value=self._convert_currency(final_input_currency,curr,amount) 
            converted_value=round(converted_value,2)
            output_dict.update({curr:converted_value})

        result_dict={
            "input":{"currency":final_input_currency,"amount":amount},
            "output":output_dict
            }

        result_json=json.dumps(result_dict,indent=4)

        #t3=timeit.default_timer()
        #print(t2-t1,',',t3-t2)
        return result_json

