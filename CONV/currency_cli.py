import argparse

import convertor

#ZABALIT TENTO KÓD DO TŘÍDY NEBO FUNKCE?

parser = argparse.ArgumentParser()
parser.add_argument('--amount', required=True, action="store", type=float)
parser.add_argument('--input_currency',required=True, action="store")
parser.add_argument('--output_currency', required=False, action="store")

args=parser.parse_args()
amount=args.amount
input_currency=args.input_currency
output_currency=args.output_currency
#print(amount,type(amount),input_currency,type(input_currency),output_currency,type(output_currency))

convertor_obj=convertor.Convertor(input_currency,amount,output_currency)

print(convertor_obj.to_convert())
