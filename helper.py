import json

forex_dict={"EUR":1.0,"AUD":1.607,"BGN":1.9558,"BRL":4.6869,"CAD":1.4867,"CHF":1.1414,"CNY":7.972,"CZK":25.765,"DKK":7.4557,"GBP":0.89078,"HKD":9.0848,"HRK":7.433,"HUF":323.04,"IDR":17304.55,"ILS":4.2251,"INR":84.6215,"ISK":129.3,"JPY":132.25,"KRW":1290.16,"MXN":21.5632,"MYR":4.8049,"NOK":9.4465,"NZD":1.7572,"PHP":62.733,"PLN":4.2796,"RON":4.6605,"RUB":76.1229,"SEK":10.33,"SGD":1.5903,"THB":37.418,"TRY":6.908,"USD":1.1606,"ZAR":16.4326}
forex_list=list(forex_dict.keys())


with open('currencies.json',encoding="utf8") as f:
    data = json.load(f)

code=[x for x in data]
code_symbol_dict={x:data[x]['symbol'] for x in code}
print(len(code_symbol_dict))



forex_dict={key:value for key,value in code_symbol_dict.items() if key in forex_list }

print(forex_dict)
print(len(forex_dict),len(forex_list))

json_forex = json.dumps(forex_dict,indent=4)
print(type(json_forex))

with open('forex_currencies.json','w',encoding="utf8") as f:
    f.write(json_forex)

#http://localhost:5000/currency_convertor?amount=10.2&input_currency=USD&output_currency=EUR