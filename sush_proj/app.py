from flask import Flask, request, render_template, jsonify
from flask_cors import CORS, cross_origin
import json
from typing import Any
app = Flask(__name__)

class Activity:
    def __init__(self,data):
        self.data = data
    
    def price_and_currency(self:Any) -> Any:
        for activity in self.data:
            if "price" in activity and "currency" in activity:
                activity['currency_price'] = f"{activity['currency']}{activity['price']}"
        return self.data
    
    def get_merged_data(self:Any, suppliers:list) -> list:
        filtered_data =[]
        for activity in self.data:
            filtered_activity = {
                "id" : activity['id'],
                "rating":activity['rating'],
                "specialOffer":activity['specialOffer'],
                "title":activity['title']
            }
            supplier_name = suppliers.get(activity['supplierId'], 'Unknown')
            filtered_activity['supplierName'] =  supplier_name
            if "currency_price" in activity:
                filtered_activity['currency_price'] = activity['currency_price']
            filtered_data.append(filtered_activity)
        return filtered_data


def read_data():
    with open('./resources/static/data/activities.json', 'r') as json_file:
        data1 = json.load(json_file)
    with open('./resources/static/data/suppliers.json', 'r') as json_file:
        data2 = json.load(json_file)

    return data1, data2

def activity_filter(data1:Any, data2:Any) -> Any:
    activity = Activity(data1)
    merge_data = activity.price_and_currency()
    suppliers = {}
    for entry in data2:
        if entry['id'] not in suppliers:
            suppliers[entry['id']] = entry['name']
    
    data = activity.get_merged_data(suppliers)
    return data

@app.route('/activity', methods=['GET'])
def display_data():
    data1, data2 = read_data()
    data = activity_filter(data1, data2)     
    return jsonify(data)


@app.route('/activity/filter', methods=['GET'])
@cross_origin()
def filter_data():
    title_filter = request.args.get('title','').strip()
    data1, data2 = read_data()
    data = activity_filter(data1, data2)
    filtered_data=[]
    if len(title_filter)>=2:
        for item in data:
            if 'title' in item and title_filter.lower() in item['title'].lower():
                filtered_data.append(item)
        
        if filtered_data is None:
            return filtered_data
     
    else: 
        filtered_data = data
    
    return jsonify(filtered_data)



# Run the app
if __name__ == '__main__':
    app.run(debug=True)