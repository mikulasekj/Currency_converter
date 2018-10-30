import unittest
from unittest import TestCase
from unittest.mock import Mock,patch
import simplejson as json
from decimal import Decimal
import logging

import convertor

logging.basicConfig(level=logging.CRITICAL)

class TestConvertor(TestCase):

    def setUp(self):
        self.test_conv_1=convertor.Convertor('CZK',15.0,'EUR')
        self.test_conv_2=convertor.Convertor('Kč',15,'€')
        self.test_conv_3=convertor.Convertor('xxx',15,'€')
        self.test_conv_3._convert_symbols()
        self.test_conv_4=convertor.Convertor('CZK',15,'xxx')
        self.test_conv_4._convert_symbols()
        self.test_conv_5=convertor.Convertor('CZK','xxx','$')
        self.test_conv_5._convert_symbols()
        self.test_conv_6=convertor.Convertor('CZK',15.0)
        
    # test if attributes of convertor object are properly created and has correct types
    def test_create_convertor(self):
        self.assertTrue(hasattr(self.test_conv_1,'input_currency'))
        self.assertIsInstance(self.test_conv_1.input_currency, str)

        self.assertTrue(hasattr(self.test_conv_1,'output_currency'))
        self.assertIsInstance(self.test_conv_1.output_currency, str)

        self.assertTrue(hasattr(self.test_conv_1,'amount'))
        self.assertIsInstance(self.test_conv_1.amount, (int,float))

        # self.assertTrue(hasattr(self.test_conv_1,'code_symbol_dict'))
        # self.assertIsInstance(self.test_conv_1.code_symbol_dict, dict)

        self.assertTrue(hasattr(self.test_conv_1,'symbol_code_dict'))
        self.assertIsInstance(self.test_conv_1.symbol_code_dict, dict)

        self.assertTrue(hasattr(self.test_conv_1,'currency_code_list'))
        self.assertIsInstance(self.test_conv_1.currency_code_list, list)

        self.assertTrue(hasattr(self.test_conv_1,'currency_symbol_list'))
        self.assertIsInstance(self.test_conv_1.currency_symbol_list, list)

    #test convert_symbols function
    def test_convert_symbols(self):
        self.assertEqual(self.test_conv_2.input_currency,'Kč')
        self.assertEqual(self.test_conv_2.output_currency,'€')
        self.test_conv_2._convert_symbols()
        self.assertEqual(self.test_conv_2.input_currency,'CZK')
        self.assertEqual(self.test_conv_2.output_currency,'EUR')

    #test check_inputs function
    def test_chek_inputs(self):
        with self.assertRaises(convertor.WrongInputCurrencyError):
             self.test_conv_3._check_inputs()
        with self.assertRaises(convertor.WrongOutputCurrencyError):
             self.test_conv_4._check_inputs()
        with self.assertRaises(ValueError):
             self.test_conv_5._check_inputs()

    @patch('forex_python.converter.CurrencyRates.get_rates')
    def test_currency_convert(self,MockRates):
        MockRates.return_value={'USD':20,'CZK':50}
        self.test_conv_1._get_actaul_rates()
        print(self.test_conv_1.forex_rates)
        result_1=self.test_conv_1._convert_currency('USD','CZK',100)
        expected_1=250
        result_2=self.test_conv_1._convert_currency('EUR','CZK',100)
        expected_2=5000
        result_3=self.test_conv_1._convert_currency('EUR','EUR',100)
        expected_3=100
        result_4=self.test_conv_1._convert_currency('CZK','EUR',100)
        expected_4=2
        result_4=self.test_conv_1._convert_currency('CZK','USD',100)
        expected_4=40
        result_4=self.test_conv_1._convert_currency('CZK','USD',0)
        expected_4=0
        self.assertEqual(expected_1,result_1)
        self.assertIsInstance(result_1, Decimal)
        self.assertEqual(expected_2,result_2)
        self.assertIsInstance(result_2, Decimal)
        self.assertEqual(expected_3,result_3)
        self.assertIsInstance(result_3, Decimal)
        self.assertEqual(expected_4,result_4)
        self.assertIsInstance(result_4, Decimal)




    #test to_convert function with mocked forex convert function with given output currency
    @patch('convertor.Convertor._convert_currency')
    def test_to_convert(self,MockConvert):
        MockConvert.return_value=60
        result_json=self.test_conv_1.to_convert()
        
        expected={"input":{"currency":"CZK","amount":15.0},"output":{"EUR":60}}
        expected_json=json.dumps(expected,indent=4)
        
        self.assertIsInstance(result_json, str)        
        self.assertEqual(expected_json,result_json)

    #test to_convert function with mocked forex convert function with no given output currency 
    @patch('convertor.Convertor._convert_currency')
    def test_to_convert(self,MockConvert):
        MockConvert.return_value=60
        result_json=self.test_conv_6.to_convert()
        #logging.debug(result_json)
        
        #Create fictive excpected dictionary of output currencies
        output_curr_expected=dict(zip(self.test_conv_6.currency_code_list,
        [MockConvert.return_value]*len(self.test_conv_6.currency_code_list)))

        #logging.debug(output_curr_expected)
        expected={"input":{"currency":"CZK","amount":15.0},"output":output_curr_expected}
        expected_json=json.dumps(expected,indent=4)
        
        self.assertIsInstance(result_json, str)        
        self.assertEqual(expected_json,result_json)
        

if __name__ == '__main__':
    unittest.main()