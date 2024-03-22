import requests
from ast import literal_eval
import pandas as pd
import numpy as np
import json
from urllib.parse import unquote, quote
import time
import os, sys
from datetime import datetime
import time
ROOT = os.getcwd()
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
from source.database.mongodb.query_mongodb import query_insert_many_data

def get_recapcha():
    output = os.popen("bash grabfood_recapcha.sh").read()
    data = output[5:].split(",")[1]
    return data[1:-1]


def get_categories(location="21.0278%2C105.8342", countryCode="VN", cityID=14):
    url = f"https://portal.grab.com/foodweb/v2/categories?latlng={location}&countryCode={countryCode}&cityID={cityID}"
    payload = {}
    headers = {
    'accept': 'application/json, text/plain, */*',
    'x-recaptcha-token': get_recapcha()
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    if "categories" in list(json_object):
        return 1, json_object["categories"]
    return 0, None


def get_citi_id_use_keyword(keyword="ho chi minh", limit=1000):
    url = f"https://food.grab.com/v1/autocomplete?component=country:VN&keyword={keyword}&limit={limit}"
    payload = {}
    headers = {
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    if "place" in list(json_object):
        return 1, json_object["place"]
    elif "places" in list(json_object):
        return 2, json_object["places"]
    return 0, None


def get_citi_id_use_location(location="21.0141184,105.7849344"):
    url = f"https://food.grab.com/v1/reverse-geo?location={location}"
    payload = {}
    headers = {
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    if "place" in list(json_object):
        return 1, json_object["place"]
    elif "places" in list(json_object):
        return 2, json_object["places"]
    return 0, None


def get_shortcuts_promo(countryCode="VN", cityID=14):
    url = f"https://portal.grab.com/foodweb/v2/category/shortcuts?countryCode={countryCode}&cityID={cityID}"
    payload = {}
    headers = {
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    if "shortcuts" in list(json_object):
        return 1, json_object["shortcuts"]
    return 0, None


def get_search_by_keyword(latlng="21.014309,105.784575", keyword="", offset=0, papesize=32, countryCode="VN"):
    url = "https://portal.grab.com/foodweb/v2/search"

    payload = json.dumps({
        "latlng": latlng,
        "keyword": keyword,
        "offset": offset,
        "pageSize": papesize,
        "countryCode": countryCode
    })
    headers = {
    'accept': 'application/json, text/plain, */*',
    'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    if "searchResult" in list(json_object):
        return 1, json_object["searchResult"]
    return 0, None


def get_list_merchants_by_shortcutid(latlng="21.014309%2C105.784575", categoryShortcutID=144, offset=0, pageSize=32):
    url = f"https://portal.grab.com/foodweb/v2/category?latlng={latlng}&categoryShortcutID={categoryShortcutID}&offset={offset}&pageSize={pageSize}"

    payload = {}
    headers = {
    'accept': 'application/json, text/plain, */*',
    'x-recaptcha-token': get_recapcha()
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    if "searchResult" in list(json_object):
        return 1, json_object
    return 0, None


def get_full_info_merchants(mer_id="5-CYMAPFUDL35KME"):
    url = f"https://portal.grab.com/foodweb/v2/merchants/{mer_id}"

    payload = {}
    headers = {
    'accept': 'application/json, text/plain, */*',
    'x-recaptcha-token': get_recapcha()
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    # print(type(json_object))
    if "merchant" in list(json_object):
        return 1, json_object
    return 0, None


def get_fixed_position_level_3(keyword_position="hanoi", limit=100):
    url = f"https://food.grab.com/v1/autocomplete?component=country%3AVN&keyword={keyword_position}&limit={limit}"
    payload = {}
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    if "places" in list(json_object):
        return 1, json_object["places"]
    return 0, None



def call_api_grab_food(collection_shop="grabfood_shop", collection_menu="grabfood_menu", path="location_level_3.csv"):
    
    data_location = np.array(pd.read_csv(path)).T[0] # lay ra 1 list danh sach cac dia diem
    for location in data_location:
        try:
            _location, fixed_position = get_fixed_position_level_3(keyword_position=quote(location))
            if _location == 1:
                for position in fixed_position:
                    try:
                        cityID = int(position["cityID"])
                        latlng = f"{position['location']['latitude']},{position['location']['longitude']}"
                        _, shortcuts_promo = get_shortcuts_promo(cityID=cityID)
                        promo_ids = [promo["id"] for promo in shortcuts_promo]
                        _, categories = get_categories(cityID=cityID, location=quote(latlng))
                        cate_ids = [cate["shortcutID"] for cate in categories]
                        shortcuts_ids = promo_ids + cate_ids # concat list
                        for shorcut_id in shortcuts_ids:
                            try:
                                offset_merchant = 0
                                total_merchant = 9999
                                while offset_merchant <= total_merchant:
                                    try:
                                        _, merchants_data = get_list_merchants_by_shortcutid(latlng=quote(latlng), 
                                                                                            categoryShortcutID=shorcut_id, offset=offset_merchant)
                                        super_categories = {
                                            "categoryName": merchants_data["categoryName"],
                                            "categoryImageURL": merchants_data["categoryImageURL"],
                                            "categoryDescription": merchants_data["categoryDescription"],
                                            "shortcutID": merchants_data["shortcutID"],
                                            "categoryImageURLFallback": merchants_data["categoryImageURLFallback"]
                                        }
                                        offset_merchant = merchants_data["searchResult"]["offset"]
                                        total_merchant = merchants_data["searchResult"]["totalCount"]
                                        
                                        merchants_full_info = []
                                        menu_full = []
                                        for mer_id in merchants_data["searchResult"]["searchMerchants"]:
                                            time.sleep(5)
                                            _status_full_info_merchants, mer_data = get_full_info_merchants(mer_id=mer_id["id"])
                                            menu_data = {"merchant_id": mer_id["id"]}
                                            if _status_full_info_merchants == 1:
                                                time_stamp = datetime.timestamp(datetime.now()) # add create
                                                mer_data["super_categories"] = super_categories
                                                mer_data["create_time"] = time_stamp

                                                menu_data["menu"] = mer_data["merchant"].pop("menu")
                                                menu_data["super_categories"] = super_categories
                                                menu_data["create_time"] = time_stamp

                                                menu_full.append(menu_data)
                                                merchants_full_info.append(mer_data)
                                            else:
                                                print(mer_id["id"]) # push lai queue de xu ly sau

                                        
                                        if len(merchants_full_info) > 0:
                                            print("merchants_full_info: ", len(merchants_full_info))
                                            status = query_insert_many_data(collection_name=collection_shop, mylist=merchants_full_info)
                                            if status["status"] == 0:
                                                print("status: ", status)
                                                print("INSERT MONGODB ERROR!!")
                                                print("DATA : ", merchants_full_info)
                                            else:
                                                print("status: ", status)
                                                print("INSERT MONGODB DONE!!")
                                        else:
                                            print("data shop not exists!")

                                        if len(menu_full) > 0:
                                            print("merchants_full_info: ", len(menu_full))
                                            status = query_insert_many_data(collection_name=collection_menu, mylist=menu_full)
                                            if status["status"] == 0:
                                                print("status: ", status)
                                                print("INSERT MONGODB ERROR!!")
                                                print("DATA : ", menu_full)
                                            else:
                                                print("status: ", status)
                                                print("INSERT MONGODB DONE!!")
                                        else:
                                            print("data menu not exists!")

                                    except Exception as err:
                                        print(f"ERROR CALL API : Unexpected {err=}, {type(err)=} - args: {err.args}")
                                        print("merchants_data : ", merchants_data)
                            except Exception as err:
                                print(f"ERROR CALL API : Unexpected {err=}, {type(err)=} - args: {err.args}")
                                print("shorcut_id : ", shorcut_id)
                    except Exception as err:
                        print(f"ERROR CALL API : Unexpected {err=}, {type(err)=} - args: {err.args}")
                        print("position : ", position)
                        print("promo_ids : ", promo_ids)
                        print("categories : ", categories)
        except Exception as err:
            print(f"ERROR CALL API : Unexpected {err=}, {type(err)=} - args: {err.args}")
            print("location : ", location)
    pass



def test_api(collection_shop="location", path="location_level_3.csv"):
    startTime = time.time()
    data_location = np.array(pd.read_csv(path)).T[0] # lay ra 1 list danh sach cac dia diem
    for location in data_location:
        try:
            _location, fixed_position = get_fixed_position_level_3(keyword_position=quote(location))
            if len(fixed_position) > 0:
                print("merchants_full_info: ", len(fixed_position))
                status = query_insert_many_data(collection_name=collection_shop, mylist=fixed_position)
                if status["status"] == 0:
                    print("status: ", status)
                    print("INSERT MONGODB ERROR!!")
                    print("DATA : ", fixed_position)
                else:
                    print("status: ", status)
                    print("INSERT MONGODB DONE!!")
            else:
                print("data shop not exists!")

        except Exception as err:
            print(f"ERROR CALL API : Unexpected {err=}, {type(err)=} - args: {err.args}")
            print("location : ", location)
        break
    endTime = time.time()
    elapsedTime = endTime - startTime
    print("Elapsed Time = %s" % elapsedTime)

    
if __name__ == "__main__":
    call_api_grab_food(collection_shop="grabfood_shop_030723", collection_menu="grabfood_menu_030723", 
                       path="/data/quangdm/ecom/crawler_go_ecom/city_data/location_level_3.csv")

    test_api(collection_shop="location_1",path="/data/quangdm/ecom/crawler_go_ecom/city_data/location_level_3.csv")
    pass