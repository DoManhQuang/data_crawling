import requests
import json
from datetime import datetime
from tqdm import tqdm
import os, sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
ROOT = os.getcwd()
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
from source.database.mongodb.query_mongodb import query_insert_many_data


def get_data_configs_cities():
    url = "https://mocha.lozi.vn/v6/configs"
    print("url get_data_configs_cities: ", url)
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response)
    # print(type(response.text))
    json_object = json.loads(response.text)
    return json_object["data"]["shippingAdministrations"]


def get_categories(superCategoryId=2, cityId=50):
    url = f"https://mocha.lozi.vn/v6/categories?superCategoryId={superCategoryId}&cityId={cityId}"
    print("url get_categories: ", url)
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    return json_object["data"]


def get_pagination_in_cityid(cityId=50, limit=24, page=1, categories=1042, superCategoryId=2):
    url = f"https://mocha.lozi.vn/v6/search/eateries?categories={categories}&cityId={cityId}&limit={limit}&page={page}&superCategoryId={superCategoryId}"
    print("url get_pagination_in_cityid : ", url)
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    return json_object["pagination"]


def get_info_basic_shop(cityId=50, limit=24, page=1, categories=1042, superCategoryId=2):
    url = f"https://mocha.lozi.vn/v6/search/eateries?categories={categories}&cityId={cityId}&limit={limit}&page={page}&superCategoryId={superCategoryId}"
    # print("url get_info_basic_shop: ", url)
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    data_shop = []
    for obj in json_object["data"]:
        shop_info = dict()
        shop_info["shop_id"] = obj["id"]
        shop_info["info_basic"] = obj
        data_shop.append(shop_info)
    return data_shop


def get_full_info_shop(username="hoaquasachdongthom"):
    url = f"https://latte.lozi.vn/v1.2/eateries/username:{username}"
    # print("url get_full_info_shop : ", url)
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    return json_object["data"]


def get_full_menu_shop(slug="hoa-qua-sach-dong-thom-quan-cau-giay-ha-noi-1639800419184589973"):
    url = f"https://mocha.lozi.vn/v6/eateries/slug:{slug}/menu"
    # print("url get_full_menu_shop : ", url)
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    return json_object["data"]


def call_api_get_info_shop(collection_name):
    cities = get_data_configs_cities()
    for city in cities:
        print("City Id: ", city["city"]["id"], " - City Name: ", city["city"]["name"])
        try:
            categories = get_categories(cityId=city["city"]["id"])
            for cate in categories:
                cate_info = {
                    "id": cate["id"],
                    "slug": cate["slug"],
                    "value": cate["value"]
                }
                print("cate info: ", cate_info)
                try:
                    pagination = get_pagination_in_cityid(cityId=city["city"]["id"], categories=cate["id"])
                    pages = int(pagination["total"]/pagination["limit"]) + 1
                    for page in tqdm(range(1, pages + 1)):
                        try:
                            my_list_shop = get_info_basic_shop(cityId=city["city"]["id"], limit=24, page=page, categories=cate["id"])
                            # my_list_tmp = []
                            # cnt_shop = 0
                            for my_shop in my_list_shop:
                                try:
                                    if my_shop["info_basic"]["username"] != '':
                                        my_shop["info_shop"] = get_full_info_shop(username=my_shop["info_basic"]["username"]) # add info shop
                                    
                                    if my_shop["info_basic"]["slug"] != '':
                                        my_shop["info_menu"] = get_full_menu_shop(slug=my_shop["info_basic"]["slug"]) # add menu shop
                                    
                                    my_shop["url_shop"] = "https://lomart.vn/" + my_shop["info_basic"]["username"] # add url shop
                                    my_shop["category_info"] = cate_info # add cate info
                                    my_shop["create_time"] = datetime.timestamp(datetime.now()) # add create
                                    # my_list_tmp.append(my_shop)
                                    # if cnt_shop == 100:
                                    #     status = query_insert_many_data(collection_name=collection_name, mylist=my_list_tmp)
                                    #     if status["status"] == 0:
                                    #         print("status: ", status)
                                    #         print("INSERT MONGODB ERROR!!")
                                    #         print("DATA : ", my_list_tmp)
                                        # else:
                                        #     my_list_tmp.clear()
                                        #     cnt_shop = 0
                                        #     print("init temp shop : ", my_list_tmp, cnt_shop)
                                except:
                                    print("ERROR CALL API info_shop, info_menu")
                                    print("my_shop['info_basic'] : ", my_shop["info_basic"]["slug"], " - ", my_shop["info_basic"]["username"])

                            if len(my_list_shop) > 0:
                                status = query_insert_many_data(collection_name=collection_name, mylist=my_list_shop)
                                if status["status"] == 0:
                                    print("status: ", status)
                                    print("INSERT MONGODB ERROR!!")
                                    print("DATA : ", my_list_shop)
                            else:
                                print("data shop not exists!")

                        except Exception as err:
                            print(f"ERROR CALL API get_info_basic_shop : Unexpected {err=}, {type(err)=} - args: {err.args}")
                except Exception as err:
                    print(f"ERROR CALL API get_pagination_in_cityid : Unexpected {err=}, {type(err)=} - args: {err.args}")
        except Exception as err:
            print(f"ERROR CALL API get_categories : Unexpected {err=}, {type(err)=} - args: {err.args}")


if __name__ == "__main__":
    call_api_get_info_shop("lomart_shop_v2")
    pass


