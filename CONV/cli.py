import argparse

import convertor

parser = argparse.ArgumentParser()
parser.add_argument('--amount', action="store", type=float)
parser.add_argument('--input_currency', action="store")
parser.add_argument('--output_currency', action="store")

args=parser.parse_args()
amount=args.amount
input_currency=args.input_currency
output_currency=args.output_currency
#print(amount,type(amount),input_currency,type(input_currency),output_currency,type(output_currency))

c=convertor.Convertor(input_currency,amount,output_currency)

print(c.to_convert())
