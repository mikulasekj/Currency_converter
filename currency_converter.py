"""This module solve the cli using argparse package"""

import argparse

import convertor


def cli_aplication():
    """Function that wraps the argparse part"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--amount', required=True, action="store", type=float,
                        help=("Required argument."
                              "The argument is for input the amount to convert"
                              "Int or float type is valid input"))
    parser.add_argument('--input_currency', required=True, action="store",
                        help=("Required argument."
                              "3-capital letter code or symbol of currency is valid input"
                              "Argument determines the currency from which will"
                              "be the amount converted."))
    parser.add_argument('--output_currency', required=False, action="store",
                        help=("Not Required argument."
                              "3-capital letter code or symbol of currency is valid input"
                              "The argument determines the currency to which"
                              "will be the amount converted. If the argument is not specified"
                              "than conversion is performed into all supported currencies."))

    args = parser.parse_args()
    amount = args.amount
    input_currency = args.input_currency
    output_currency = args.output_currency

    convertor_obj = convertor.Convertor()

    print(convertor_obj.to_convert(input_currency, amount, output_currency))

if __name__ == '__main__':
    cli_aplication()
