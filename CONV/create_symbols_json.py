import json

with open('currencies.json',encoding="utf8") as f:
    data = json.load(f)

Curr_code_list=data.keys()
# print(type(Curr_code_list))
# print(Curr_code_list)

code_symbol_dict={x:data[x]['symbol'] for x in Curr_code_list}
print(type(code_symbol_dict))
print(code_symbol_dict)

json_code_symbol = json.dumps(code_symbol_dict,indent=4)
with open('code_symbol.json','w',encoding="utf8") as f:
    f.write(json_code_symbol)