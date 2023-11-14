import json 
import msgpack
import os

with open("products_21.json") as file:
    data = json.load(file)
    
    products = dict()
    
    for item in data:
        if item['name'] in products:
            products[item['name']].append(item['price'])
        else:
            products[item['name']] = list()
            products[item['name']].append(item['price'])
    
    result = list()

    for name, prices in products.items():
        summ_price = 0
        average_summ_price = 0
        max_price = prices[0]
        min_price = prices[0] 
        size = len(prices)
        for price in prices:
            summ_price += price
            max_price = max(max_price, price)
            min_price = min(min_price, price)
            
        result.append({
           "name": name,
           "max_price": max_price,
           "min_price": min_price,
           "avearge_price": summ_price / size
        })     
        
with open("result_prices.json", "w") as r_json:
    r_json.write(json.dumps(result))
    
with open("result_prices.msgpack", "wb") as r_msgpack:  # "wb" - запись бинарного формата
   r_msgpack.write(msgpack.dumps(result))


print(f"json     = {os.path.getsize('result_prices.json')}")
print(f"msgpack  = {os.path.getsize('result_prices.msgpack')}")