from flask import Flask,Response
from flask_restful import Resource, Api, reqparse,abort
import requests

import convertor

app = Flask(__name__)
api = Api(app)

def abort_if_input_currency_not_exist():
    abort(404, message="The input currency is not supported")

def abort_if_ouput_currency_not_exist():
    abort(404, message="The ouput currency is not supported")

def abort_if_request_fail():
    abort(404, message='Fixer api failed - not latest rates may be used for conversion')

class Inputs(Resource):
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('amount', required=True, action="store", type=float)
        parser.add_argument('input_currency',required=True, action="store")
        parser.add_argument('output_currency',required=False, action="store")

        args=parser.parse_args()
        amount=args.amount
        input_currency=args.input_currency
        output_currency=args.output_currency
        
        convertor_obj=convertor.Convertor()
        try:
            response=Response(response=convertor_obj.to_convert(input_currency,amount,output_currency))
        except convertor.WrongInputCurrencyError:
            abort_if_input_currency_not_exist()
        except convertor.WrongOutputCurrencyError:
            abort_if_ouput_currency_not_exist()
        except (convertor.FixerApiIsNotAvailableError, requests.exceptions.ConnectionError):
            abort_if_request_fail()

            
        response.content_type='application/json'
        return response
        
app.config['ERROR_404_HELP'] = False

api.add_resource(Inputs, '/currency_converter',endpoint='currency_converter')
#http://localhost:5000/currency_converter?amount=10.2&input_currency=USD&output_currency=EUR
if __name__ == '__main__':
    app.run(debug=False)