from forex_python.converter import CurrencyRates
from forex_python.converter import CurrencyCodes
import json

class convertor:

    def __init__(self,input_currency,amount,output_currency=None):
        
        self.input_currency=input_currency
        self.output_currency=output_currency
        self.amount=amount

    # load the json file with currencies codes and symbols
        with open('currencies.json',encoding="utf8") as f:
            data = json.load(f)

        code=[x for x in data]
        self.code_symbol_dict={x:data[x]['symbol'] for x in code}

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
            
            
    def convert(self):
        
        c=CurrencyRates()
        self.convert_symbols()
        output_dict={}     

    # if the output value is not given the whole known currencies are shown
        if self.output_currency==None:
            for curr in self.currency_code_list:
                try:
                    converted_value=c.convert(self.input_currency,curr,self.amount)
                except:
                    continue
                
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

