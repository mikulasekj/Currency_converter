import unittest
from unittest import TestCase
from unittest.mock import Mock,patch
import simplejson as json
from decimal import Decimal


import convertor

class TestConvertor(TestCase):

    def setUp(self):
        self.test_conv_1=convertor.Convertor()
        
    # test if attributes of convertor object are properly created and has correct types
    def test_create_convertor(self):
        self.assertTrue(hasattr(self.test_conv_1,'base_currency'))
        self.assertIsInstance(self.test_conv_1.base_currency, str)

        self.assertTrue(hasattr(self.test_conv_1,'code_symbol_dict'))
        self.assertIsInstance(self.test_conv_1.code_symbol_dict, dict)

        self.assertTrue(hasattr(self.test_conv_1,'symbol_code_dict'))
        self.assertIsInstance(self.test_conv_1.symbol_code_dict, (dict))

    #test convert_symbols function
    def test_create_and_check_final_input_curr(self):
        self.assertEqual(self.test_conv_1._create_and_check_final_input_curr('Kč'),'CZK')
        self.assertEqual(self.test_conv_1._create_and_check_final_input_curr('€'),'EUR')
        with self.assertRaises(convertor.WrongInputCurrencyError):
            self.test_conv_1._create_and_check_final_input_curr('xx')
    
    def test_create_and_check_final_output_curr(self):
        self.assertEqual(self.test_conv_1._create_and_check_final_output_curr('Kč'),['CZK'])
        self.assertEqual(self.test_conv_1._create_and_check_final_output_curr('€'),['EUR'])
        expected_1=["USD","CAD","AUD","BRL","HKD","MXN","NZD","SGD"]
        self.assertEqual(self.test_conv_1._create_and_check_final_output_curr('$'),expected_1)
        with self.assertRaises(convertor.WrongOutputCurrencyError):
            self.test_conv_1._create_and_check_final_output_curr('xx')
        

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
    def test_to_convert_specified_unique_output_curerncy(self,MockConvert):
        MockConvert.return_value=60
        result_json=self.test_conv_1.to_convert('CZK',15.0,'EUR')
        
        expected={"input":{"currency":"CZK","amount":15.0},"output":{"EUR":60}}
        expected_json=json.dumps(expected,indent=4)
        
        self.assertIsInstance(result_json, str)        
        self.assertEqual(expected_json,result_json)

    #test to_convert function with mocked forex convert function with no given output currency 
    @patch('convertor.Convertor._convert_currency')
    def test_to_convert_not_specified_output_curerncy(self,MockConvert):
        MockConvert.return_value=60
        result_json=self.test_conv_1.to_convert('CZK',15.0,None)
        
        output_curr_expected=dict(zip(self.test_conv_1.code_symbol_dict.keys(),
        [MockConvert.return_value]*len(self.test_conv_1.code_symbol_dict.keys())))

        expected={"input":{"currency":"CZK","amount":15.0},"output":output_curr_expected}
        expected_json=json.dumps(expected,indent=4)
        
        self.assertIsInstance(result_json, str)        
        self.assertEqual(expected_json,result_json)
        

if __name__ == '__main__':
    unittest.main()