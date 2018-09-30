from forex_python.converter import CurrencyRates

#class convertor:

#modify for decimal
def convert(input_currency,output_currency,amount):
    c=CurrencyRates()
    converted_value=c.convert(input_currency,output_currency,amount)
    #(return converted currency as float type)
    return converted_value