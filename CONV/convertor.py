from forex_python.converter import CurrencyRates
from forex_python.converter import CurrencyCodes
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
    def __init__(self,input_currency,amount,output_currency=None):
        
        self.input_currency=input_currency
        self.output_currency=output_currency
        self.amount=amount

        self.base_currency='EUR'

        t1=timeit.default_timer()
        # load the json file with currencies codes and symbols
        with open('forex_currencies.json',encoding="utf8") as f:
            code_symbol_dict = json.load(f)
        

        #create dictionary with key as a symbol and code as a value
        self.symbol_code_dict={key:value for value,key in code_symbol_dict.items()}

        #create lists of currencies symbols and codes

        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ODSTRANIT LISTY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        self.currency_code_list=list(code_symbol_dict.keys())
        self.currency_symbol_list=list(self.symbol_code_dict.keys())
        t2=timeit.default_timer()
        #print(t2-t1)

    #function to convert input/outpu symbols into correspoding code of currency. 
    def _convert_symbols(self):
        if self.input_currency in self.currency_symbol_list:
            self.input_currency=self.symbol_code_dict[self.input_currency]  

        if self.output_currency in self.currency_symbol_list:
            self.output_currency=self.symbol_code_dict[self.output_currency]

    def _check_inputs(self):
        try:
            if self.input_currency not in self.currency_code_list:
                raise WrongInputCurrencyError()
            if self.output_currency not in self.currency_code_list and self.output_currency!=None:
                raise WrongOutputCurrencyError()
            if not isinstance(self.amount ,(int,float)):
                raise ValueError
        except WrongInputCurrencyError as e:
            print(e.message)
            raise
        except WrongOutputCurrencyError as e:
            print(e.message)
            raise
        except ValueError:
            print('Amount must be a number' )
            raise

    def _get_actaul_rates(self):
        
        self.forex_rates=CurrencyRates().get_rates(self.base_currency)

    def _convert_currency(self,input_curr,output_curr,amount):
        """Covnert input currency to output currency using base_currency EUR"""

        amount_in_decimal=Decimal(str(amount))

        if input_curr==output_curr:
            converted_currency=amount_in_decimal

        elif input_curr==self.base_currency:
            converted_currency=amount_in_decimal*Decimal(str(self.forex_rates[output_curr]))

        elif output_curr==self.base_currency:
            converted_currency=amount_in_decimal/Decimal(str(self.forex_rates[input_curr]))

        else:
            base_amount=amount_in_decimal/Decimal(str(self.forex_rates[input_curr]))
            converted_currency=base_amount*Decimal(str(self.forex_rates[output_curr]))

        return converted_currency


        
            
          
    def to_convert(self):
        """Use "private" functions _get_actual_rates(),_convert_symbols(),_check_outputs() and _conver_currency() 
           to performe all the neccesary stuff to convert given inpits. 
           If there is no output currency the input currency is converted into all possilbew currencies
        """
        
        self._get_actaul_rates()
        
        t1=timeit.default_timer()
        
        self._convert_symbols()
        self._check_inputs()
        output_dict={}  
        t2=timeit.default_timer()
         

        # if the output value is not given the whole known(by forex) currencies are outputed
        if self.output_currency==None:
            for curr in self.currency_code_list:
                # if the currency code is not support by forex-python(forex raise the error) than skip the currency
                
                converted_value=self._convert_currency(self.input_currency,curr,self.amount) 
                converted_value=round(converted_value,2)
                output_dict.update({curr:converted_value})
                

        else:
            converted_value=self._convert_currency(self.input_currency,self.output_currency,self.amount)
            converted_value=round(converted_value,2)
            output_dict={self.output_currency:converted_value}

        result_dict={
            "input":{"currency":self.input_currency,"amount":self.amount},
            "output":output_dict
            }

        result_json=json.dumps(result_dict,indent=4)

        t3=timeit.default_timer()
        #print(t2-t1,',',t3-t2)
        return result_json

