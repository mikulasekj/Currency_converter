from flask import Flask,Response
from flask_restful import Resource, Api, reqparse,abort

import convertor

app = Flask(__name__)
api = Api(app)

def abort_if_input_currency_not_exist():
    abort(404, message="The input currency is not supported")

def abort_if_ouput_currency_not_exist():
    abort(404, message="The ouput currency is not supported")

class Inputs(Resource):
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('amount', action="store", type=float)
        parser.add_argument('input_currency', action="store")
        parser.add_argument('output_currency', action="store")

        args=parser.parse_args()
        amount=args.amount
        input_currency=args.input_currency
        output_currency=args.output_currency
        
        c=convertor.Convertor(input_currency,amount,output_currency)
        try:
            r=Response(response=c.to_convert())
        except convertor.WrongInputCurrencyError:
            abort_if_input_currency_not_exist()
        except convertor.WrongOutputCurrencyError:
            abort_if_ouput_currency_not_exist()

            
        r.content_type='application/json'
        return r
        
app.config['ERROR_404_HELP'] = False

api.add_resource(Inputs, '/currency_convertor',endpoint='currency_convertor')
#http://localhost:5000/currency_convertor?amount=10.2&input_currency=USD&output_currency=EUR
if __name__ == '__main__':
    app.run(debug=False)