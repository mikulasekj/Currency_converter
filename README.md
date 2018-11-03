## Main purpose and descritpion of the project
The repsoitory contains program for converting currencies which can be managed via web api application or cli aplication.

### Particular files purposes:

- convertor.py

  - All the conversion is taking place here in convertor class
  - Store the JSON file with rates downloaded from fixer.io as fixer_rates.json. If the fixer api failed the 
    latestly stored fixer_rates.json file is used for convertion. In this case warnig that the rates could not be updated is shown as a part of relusts
  - If symbols of currency is given as an input or output convert the symbol on corresponding 3-letter currency code
  using the code-symbol dictionary stored permanetly in code_symbol.json file
  - Result is JSON file in format as per task entry
  
 - currency_converter.py
   - parse the argument from the terminal and pass them to convertor object which perform the conversion. Finaly print the results
   
 - currency_converter_api.py
   - parse the argument from get request and pass them to convertor object which perform the conversion. Finaly send the results as response
 
 - code_symbol.json
   - store the key-value pairs to mapping symbols currencies to codes of currencies
   
 - fixer_rates.json
   - store the lates valid key-value pairs with rates for each currency considering the base cuurecny
   
 - tests.py
   - perform chosen tests on chosen methods of convertor class
   
For more detail information see particular classes or methods docstrings
