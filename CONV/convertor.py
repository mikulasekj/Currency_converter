from forex_python.converter import CurrencyRates
from forex_python.converter import CurrencyCodes
import requests
import timeit

from decimal import Decimal

import simplejson as json

class WrongInputCurrencyError(Exception):
    def __init__(self):
        self.message='The input currency is not supported.'
        

class WrongOutputCurrencyError(Exception):
    def __init__(self):
        self.message='The output currency is not supported.'
        
    
class Convertor:

    #initialize the object of convertor class with given atributes
    def __init__(self):

        self.base_currency='EUR'

        #t1=timeit.default_timer()
        # load the json file with currencies codes and symbols
        with open('code_symbol.json',encoding="utf8") as f:
            self.code_symbol_dict = json.load(f)
        
        with open('fixer_rates.json',encoding="utf8") as f:
            rates_json = json.load(f)
        
        print(rates_json['timestamp'])

        self.rates_dict=rates_json['rates']

        

        
        #create dictionary with key as a symbol and code as a value
        self.symbol_code_dict={key:value for value,key in self.code_symbol_dict.items()}

        #t2=timeit.default_timer()
        #print(t2-t1)

    
    def _create_and_check_final_input_curr(self,given_input_currency):
        
        if given_input_currency in self.symbol_code_dict.keys():
            final_input_currency=self.symbol_code_dict[given_input_currency]
            
        elif given_input_currency in self.code_symbol_dict.keys():
            final_input_currency=given_input_currency
            
        else:
            raise WrongInputCurrencyError()

        return final_input_currency
        
        

    def _create_and_check_final_output_curr(self,given_output_currency):
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
            raise WrongOutputCurrencyError()
        
        final_output_curr_list=list(set(semifinal_output_curr_list)&set(self.rates_dict.keys()))
        if not final_output_curr_list:
            raise WrongOutputCurrencyError()
        
        return final_output_curr_list
        

    #DOPLNIT VYJÍMKY - co kdz6 dojdou pokusz  A OTESTOVAT!!!!!!!!
    #KAM UKLÁDAT???????????
    def _get_actaul_rates(self):
        "rates are actualized 1/hour"

        base_url='http://data.fixer.io/api/latest'
        access_key='access_key=1f45f76495a5436a9a6fabca5884f2a2'
        rate_url=(base_url+'?'+access_key)       
        
        #self.forex_rates=CurrencyRates().get_rates(self.base_currency)
        fixer_rates_response = requests.get(rate_url)
        fixer_rates_json=fixer_rates_response.json()

        #latest_timestamp=fixer_rates_json[timestamp]
        with open('fixer_rates.json','w',encoding="utf8") as f:
            json.dump(fixer_rates_json,f,indent=4)

        


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

