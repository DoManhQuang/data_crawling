import requests
import json
from datetime import datetime
from tqdm import tqdm
import numpy as np
import os, sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import concurrent.futures
import threading
import time
ROOT = os.getcwd()
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT)) 
from source.database.mongodb.query_mongodb import query_insert_many_data

def get_statistics_by_city_category():
    url = "https://gappapi.deliverynow.vn/api/delivery/get_statistics_by_city_category"
    payload = {}
    headers = {
    'Authority': 'gappapi.deliverynow.vn',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Origin': 'https://shopeefood.vn',
    'Pragma': 'no-cache',
    'Referer': 'https://shopeefood.vn/',
    'Sec-Ch-Ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'X-Foody-Access-Token': '',
    'X-Foody-Api-Version': '1',
    'X-Foody-App-Type': '1004',
    'X-Foody-Client-Id': '',
    'X-Foody-Client-Language': 'vi',
    'X-Foody-Client-Type': '1',
    'X-Sap-Ri':'',
    'X-Foody-Client-Version': '3.0.0'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data_citi_ids = []
    json_object = json.loads(response.text)
    # print(list(json_object))
    if "result" in list(json_object):
        if json_object["result"] == "success":
            for city in json_object["reply"]["cities"]:
                data_citi_ids.append(city["city_id"])
        return True, json_object["result"], data_citi_ids
    return False, None, None


   
def get_list_res_ids_search_global(city_id=273, token="xxx", foody_services=[5]):
    url = "https://gappapi.deliverynow.vn/api/delivery/search_global"
    payload = json.dumps({
    "category_group": 1,
    "city_id": city_id,
    "delivery_only": True,
    "keyword": "",
    "foody_services": foody_services,
    "full_restaurant_ids": True
    })
    headers = {
    'X-Foody-Access-Token': token,
    'X-Foody-Api-Version': '1',
    'X-Foody-App-Type': '1004',
    'X-Foody-Client-Id': '',
    'X-Foody-Client-Language': 'vi',
    'X-Foody-Client-Version': '3.0.0',
    'X-Foody-Client-Type': '1',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    data_restaurant_ids = []
    if json_object["result"] == "success":
        for service_type in json_object["reply"]["search_result"]:
            data_restaurant_ids.append(service_type["restaurant_ids"])
    return json_object["result"], data_restaurant_ids


def get_get_delivery_dishes(request_id=295087, token="xxx"):
    url = f"https://gappapi.deliverynow.vn/api/dish/get_delivery_dishes?id_type=2&request_id={request_id}"
    payload = ""
    headers = {
    'X-Foody-Access-Token': token,
    'X-Foody-Api-Version': '1',
    'X-Foody-App-Type': '1004',
    'X-Foody-Client-Id': '',
    'X-Foody-Client-Language': 'vi',
    'X-Foody-Client-Version': '3.0.0',
    'X-Foody-Client-Type': '1',
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    if json_object["result"] == "success":
        return json_object["result"], json_object["reply"]["menu_infos"]
    return json_object["result"], []


def get_info_basic_shops(restaurant_ids=[1156744, 767979], token="xxx"):
    url = "https://gappapi.deliverynow.vn/api/delivery/get_infos"
    payload = json.dumps({
    "restaurant_ids": restaurant_ids
    })
    headers = {
    'X-Foody-Access-Token': token,
    'X-Foody-Api-Version': '1',
    'X-Foody-App-Type': '1004',
    'X-Foody-Client-Id': '',
    'X-Foody-Client-Language': 'vi',
    'X-Foody-Client-Version': '3.0.0',
    'X-Foody-Client-Type': '1',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    data_shop_info = []
    if json_object["result"] == "success":
        for shop_info in json_object["reply"]["delivery_infos"]:
            shop_info["create_time"] = datetime.timestamp(datetime.now())
            status_menu, menu_info = get_get_delivery_dishes(request_id=shop_info["delivery_id"], token=token)
            if status_menu == "success":
                shop_info["menu_info"] = menu_info
            data_shop_info.append(shop_info)
    return json_object["result"], data_shop_info

def get_browsing_delivery_ids(city_id=217, foody_services=[5], token="xxx"):
    url = "https://gappapi.deliverynow.vn/api/delivery/get_browsing_ids"
    payload = json.dumps({
    "city_id": city_id,
    "sort_type": 30,
    "foody_services": foody_services
    })
    headers = {
    'X-Foody-Access-Token': token,
    'X-Foody-Api-Version': '1',
    'X-Foody-App-Type': '1004',
    'X-Foody-Client-Id': '',
    'X-Foody-Client-Language': 'vi',
    'X-Foody-Client-Version': '3.0.0',
    'X-Foody-Client-Type': '1',
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    if json_object["result"] == "success":
        return json_object["result"], json_object["reply"]["delivery_ids"]
    return json_object["result"], []


def get_detail_delivery(request_id=15400, token="xxx"):
    url = f"https://gappapi.deliverynow.vn/api/delivery/get_detail?id_type=2&request_id={request_id}"

    payload = ""
    headers = {
    'X-Foody-Access-Token': token,
    'X-Foody-Api-Version': '1',
    'X-Foody-App-Type': '1004',
    'X-Foody-Client-Id': '',
    'X-Foody-Client-Language': 'vi',
    'X-Foody-Client-Version': '3.0.0',
    'X-Foody-Client-Type': '1',
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    if json_object["result"] == "success":
        return json_object["result"], json_object["reply"]["delivery_detail"]
    return json_object["result"], []


def call_api_get_info_shop_use_res_ids_threading(collection_name="xxx", token="xxx", max_workers=5):
    flag, status_city, cities = get_statistics_by_city_category()
    if not flag:
        print("Call API get_statistics_by_city_category => Fail")
        return
    if status_city == "success":
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for city_idx in tqdm(range(len(cities))):
                # city_id = cities[city_idx]
                future = executor.submit(process_city, collection_name, token,city_id=cities[city_idx])
                futures.append(future)
            for future in concurrent.futures.as_completed(futures):
                try:
                    print(future.result())
                except Exception as err:
                    print(f"ERROR CALL API : Unexpected {err=}, {type(err)=} - args: {err.args}")
                    
    else:
        print("ERROR CALL API status city : ", status_city)
        print("city id: ", cities[city_idx])
    
def call_api_get_info_shop_use_res_ids(collection_name="xxx", token="xxx"):
    status_city, cities = get_statistics_by_city_category()
    if status_city == "success":
        for city_idx in tqdm(range(0, len(cities))):
            try:
                status_res_ids, list_res_ids = get_list_res_ids_search_global(city_id=cities[city_idx], token=token)
                if status_res_ids == "success":
                    for res_ids in list_res_ids:
                        status_shop, my_list_shop = get_info_basic_shops(restaurant_ids=res_ids, token=token)
                        if status_shop == "success":
                            status = query_insert_many_data(collection_name=collection_name, mylist=my_list_shop)
                            if status["status"] == 0:
                                print("status : ", status)
                                print("INSERT MONGODB ERROR!!")
                                print("DATA : ", my_list_shop)
                            else:
                                print("INSERT MONGODB PASS!!")
                        else:
                            print("ERROR CALL API status_shop : ", status_shop)
                else:
                    print("ERROR CALL API status_res_ids : ", status_res_ids)
            except Exception as err:
                print(f"ERROR CALL API : Unexpected {err=}, {type(err)=} - args: {err.args}")
    else:
        print("ERROR CALL API status city : ", status_city)
        print("city id: ", cities[city_idx])



def call_api_get_info_shop_use_deli_ids(collection_name="xxx", token="xxx"):
    flag, status_city, cities = get_statistics_by_city_category()
    if not flag:
        print("Call API get_statistics_by_city_category => Fail")
        return
    if status_city == "success":
        for city_idx in range(0, len(cities)):
            try:
                status_deli, delivery_ids = get_browsing_delivery_ids(city_id=cities[city_idx], foody_services=[5], token=token)
                if status_deli == "success":
                    my_list_shop = []
                    for deli_id in delivery_ids:
                        status_shop, shop_info = get_detail_delivery(request_id=deli_id, token=token)
                        if status_shop == "success":
                            shop_info["create_time"] = datetime.timestamp(datetime.now()) # add create
                            
                            status_menu, menu_info = get_get_delivery_dishes(request_id=deli_id, token=token) # get menu
                            if status_menu == "success":
                                shop_info["menu_info"] = menu_info # add menu
                            else:
                                print("ERROR CALL API status_menu : ", status_menu)
                                print("deli_id : ", deli_id)
                            
                            my_list_shop.append(shop_info)

                        else:
                            print("ERROR CALL API status_shop : ", status_shop)
                            print("deli_id : ", deli_id)

                    status = query_insert_many_data(collection_name=collection_name, mylist=my_list_shop) # add list shop
                    if status["status"] == 0:
                        print("status: ", status)
                        print("INSERT MONGODB ERROR!!")
                        print("DATA : ", my_list_shop)
                else:
                    print("ERROR CALL API status_deli : ", status_deli)
                    print("delivery_ids : ", np.array(delivery_ids).shape)
                    print("list delivery_ids : ", delivery_ids)
            except Exception as err:
                print(f"ERROR CALL API : Unexpected {err=}, {type(err)=} - args: {err.args}")
    else:
        print("ERROR CALL API status city : ", status_city)
        print("city id: ", cities[city_idx])

def process_city(collection_name, token,city_id):
    status_res_ids, list_res_ids = get_list_res_ids_search_global(city_id=city_id, token=token)
    if status_res_ids == "success":
        for res_ids in list_res_ids:
            status_shop, my_list_shop = get_info_basic_shops(restaurant_ids=res_ids, token=token)
            if status_shop == "success":
                status = query_insert_many_data(collection_name=collection_name, mylist=my_list_shop)
                if status["status"] == 0:
                    print("status : ", status)
                    print("INSERT MONGODB ERROR!!")
                    # print("DATA : ", my_list_shop)
                else:
                    print("INSERT MONGODB PASS!!")
            else:
                print("ERROR CALL API status_shop : ", status_shop)
    else:
        print("ERROR CALL API status_res_ids : ", status_res_ids)

if __name__ == "__main__":
    # call_api_get_info_shop_use_deli_ids(collection_name="shopeefood_test_6_6", 
    #                                     token="17fcb31a031f94c1ff5a79f8b3488d30e80e9b9f28c9730d4b6e2b58cc5d4b3d7585b37fc1a2d454b9f5890809d8dc0fe2289d953eca5f4bbdc0afb6b73b2d1e")

    call_api_get_info_shop_use_res_ids_threading(collection_name="shopefood_6_6_t2",
                                       token="17fcb31a031f94c1ff5a79f8b3488d30e80e9b9f28c9730d4b6e2b58cc5d4b3d7585b37fc1a2d454b9f5890809d8dc0fe2289d953eca5f4bbdc0afb6b73b2d1e",
                                       max_workers=4)
    
    # call_api_get_info_shop_use_res_ids(collection_name="shopefood_6_6_t2",
    #                                    token="17fcb31a031f94c1ff5a79f8b3488d30e80e9b9f28c9730d4b6e2b58cc5d4b3d7585b37fc1a2d454b9f5890809d8dc0fe2289d953eca5f4bbdc0afb6b73b2d1e")
    # # print(get_browsing_delivery_ids(city_id=272))

    # print(get_detail_delivery(request_id=175065))

    pass