import unittest

import convertor

class TestConvertor(unittest.TestCase):

    def setUp(self):
        self.test_conv_1=convertor.convertor('CZK',15,'EUR')
        self.test_conv_2=convertor.convertor('Kč',15,'€')
        self.test_conv_3=convertor.convertor('xxx',15,'€')
        self.test_conv_3.convert_symbols()
        self.test_conv_4=convertor.convertor('CZK',15,'xxx')
        self.test_conv_4.convert_symbols()
        self.test_conv_5=convertor.convertor('CZK','xxx','$')
        self.test_conv_5.convert_symbols()
        #pass
    # test if attributes of convertor object are properly created and has correct types
    def test_create_convertor(self):
        self.assertTrue(hasattr(self.test_conv_1,'input_currency'))
        self.assertIsInstance(self.test_conv_1.input_currency, str)

        self.assertTrue(hasattr(self.test_conv_1,'output_currency'))
        self.assertIsInstance(self.test_conv_1.output_currency, str)

        self.assertTrue(hasattr(self.test_conv_1,'amount'))
        self.assertIsInstance(self.test_conv_1.amount, (int,float))

        self.assertTrue(hasattr(self.test_conv_1,'code_symbol_dict'))
        self.assertIsInstance(self.test_conv_1.code_symbol_dict, dict)

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
        self.test_conv_2.convert_symbols()
        self.assertEqual(self.test_conv_2.input_currency,'CZK')
        self.assertEqual(self.test_conv_2.output_currency,'EUR')

    #test check_inputs function
    def test_chek_inputs(self):
        with self.assertRaises(convertor.WrongInputCurrencyError):
             self.test_conv_3.check_inputs()
        with self.assertRaises(convertor.WrongOutputCurrencyError):
             self.test_conv_4.check_inputs()
        with self.assertRaises(ValueError):
             self.test_conv_5.check_inputs()



        

if __name__ == '__main__':
    unittest.main()