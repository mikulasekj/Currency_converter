from forex_python.converter import CurrencyRates
from forex_python.converter import CurrencyCodes

import logging

logging.basicConfig(level=logging.CRITICAL)

import json

class WrongInputCurrencyError(Exception):
    def __init__(self):
        self.message='Wrong inputs.'

class WrongOutputCurrencyError(Exception):
    def __init__(self):
        self.message='Wrong outputs.'

class convertor:

    def __init__(self,input_currency,amount,output_currency=None):
        
        self.input_currency=input_currency
        self.output_currency=output_currency
        self.amount=amount

        logging.debug("Inputs: {},{},{})".format(self.input_currency, self.output_currency,self.amount))

    # load the json file with currencies codes and symbols
        with open('forex_currencies.json',encoding="utf8") as f:
            data = json.load(f)

        # code=[x for x in data]
        # self.code_symbol_dict={x:data[x]['symbol'] for x in code}
        self.code_symbol_dict=data

    #create dictionary with key as a symbol and code as a value
        self.symbol_code_dict={key:value for value,key in self.code_symbol_dict.items()}

    #create lists of currencies symbols and codes
        self.currency_code_list=list(self.code_symbol_dict.keys())
        self.currency_symbol_list=list(self.symbol_code_dict.keys())

    #if there are any currency symbols as input or ouput, than the function transform them into correspoding code
    def convert_symbols(self):
        if self.input_currency in self.currency_symbol_list:
            self.input_currency=self.symbol_code_dict[self.input_currency]  

        if self.output_currency in self.currency_symbol_list:
            self.output_currency=self.symbol_code_dict[self.output_currency]

    def check_inputs(self):
        logging.debug("Inputs: {},{},{})".format(self.input_currency,self.amount, self.output_currency))
        try:
            if self.input_currency not in self.currency_code_list:
                raise WrongInputCurrencyError
            if self.output_currency not in self.currency_code_list and self.output_currency!=None:
                raise WrongOutputCurrencyError
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
            
            
    def toConvert(self):
        
        c=CurrencyRates()
        self.convert_symbols()
        self.check_inputs()
        output_dict={}     

    # if the output value is not given the whole known(by forex) currencies are shown
        if self.output_currency==None:
            for curr in self.currency_code_list:
                # if the currency code is not support by forex-python(forex raise the error) than skip the currency
                
                converted_value=c.convert(self.input_currency,curr,self.amount) 
                output_dict.update({curr:converted_value})

        else:
            converted_value=c.convert(self.input_currency,self.output_currency,self.amount)
            output_dict={self.output_currency:converted_value}

        result_dict={
            "input":{"currency":self.input_currency,"amount":self.amount},
            "output":output_dict
            }

        result_json=json.dumps(result_dict,indent=4)

        return result_json

