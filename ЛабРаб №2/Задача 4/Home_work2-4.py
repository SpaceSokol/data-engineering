import json
import pickle
import io

with open("price_info_21.json") as file:
    data_new_prices = json.load(file)
    #for i in data_new_prices:
      #  print(i['method'])

with open("products_21.pkl", "rb") as file:
    data_old_prices = pickle.load(file)

   # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  #  for i in data_old_prices:
        #print((i))
    #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
   # print(data_old_prices)

def method(data_new_prices, data_old_prices):
    for i in data_new_prices:
        for j in data_old_prices:
            if i['name'] == j['name']:
                if i["method"] == 'sum':
                    j["price"] += i["param"]
                elif i["method"] == 'sub':
                    j["price"] -= i["param"]
                elif i["method"] == 'percent+':
                    j["price"] *= (1 + i["param"])
                elif i["method"] == 'percent-':
                    j["price"] *= (1 - i["param"])
    # округлим цены до двух знаков
                # j["price"] = round(j["price"], 2)
                result = round(j["price"], 2)
    return result

new_data = []
my_dict = dict()

for item_new in data_new_prices:
    for key in item_new:
        if key == "name":
            str_name = item_new[key]
            result = method(data_new_prices, data_old_prices)
            new_data.append({"name": item_new[key], "new_price":result})    # куда то сюда добавить метод
            # new_data.append({"new_price":result})

            my_dict = new_data

#with open('result_prices.pkl', 'wb') as f:
  #  pickle.dump(my_dict, f)

