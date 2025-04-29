from fastapi import FastAPI, Query
import os, sys
from datetime import datetime, timezone
from tqdm import tqdm

ROOT = os.getcwd()
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
    
import source.database.mongodb.query_mongodb as query_mongodb
import source.ecom_api.lomart as lomart
# import source.ecom_api.shopee_food as shopee_food
from source.ecom_api.shopee_food import get_statistics_by_city_category
lormart = "lomart_shop_v2"
shopee_food = "shopefood_6_6_t2"
app = FastAPI()

@app.get("/")
def ping():
    return{
        "hello": "world"
    }
# Tốp 5 quán ăn có rating cao nhất
@app.get("/top5-rating/{location_url}/{k}")
async def tbl_rating(location_url: str, k: int):
    responses = query_mongodb.top_k_rating(location_url=location_url, k=k)
    return responses
 

 
    
@app.get("/info-menu/{infor_basic}")        
async def tbl_info(city : str):
    responses = query_mongodb.info_basic(city = city)
    return responses


@app.get("/allapi")        
async def tbl_api(location_url: str = Query(default= "", alias= "location")):
    responses = query_mongodb.call_api(location_url = location_url)
    return responses
# Số lượng quán ăn trong shopee theo id của thành phố của shopeefood
@app.get("/get-quantity-shopee") 
def count_shopee_food(cityId: str = ""):
    responses = query_mongodb.count_shopee(city_id= cityId)
    
    return {
        "quantity": responses
    }
# Số lượng quán ăn theo id của thành phố của lomart
@app.get("/get-quantity-lomart") 
def count_lomarts(city_id: str = ""):
    responses = query_mongodb.count_lomart(city_id= city_id)
    
    return {
        "quantity": responses
    }
# Liệt kê danh sách từng thành phố có bao nhiêu quán ăn trong lomart
@app.get("/get-quantity-shop-city-lomart") 
def count_city_lomart():
    data={}
    cities = lomart.get_data_configs_cities()
    for city in cities:
        print("City Id: ", city["city"]["id"], " - City Name: ", city["city"]["name"])
        data[city["city"]["name"]] = query_mongodb.count_lomart(city_id=str(city["city"]["id"]))
    
    return {
        "quantity": data
    }

# Liệt kê danh sách từng thành phố có bao nhiêu quán ăn trong shopeefood
    
@app.get("/get-quantity-shop-city-shopeefood") 
def count_city_shopeefood():
    data={}
    flag, status_city, cities = get_statistics_by_city_category()
    if flag:
        if status_city == "success":
            for city_idx in tqdm(range(0, len(cities))):
                city_id=cities[city_idx]
                print("City id ABC: ",city_id)
                data[city_id] = query_mongodb.count_shopee(city_id=str(city_id))
    else:
        print("CALL API get_statistics_by_city_category ==> Fail")
    return {
        "quantity": data
    }
    
# Liệt kê số lượng quán ăn theo danh mục sản phẩm trong 1 thành phố
# Lomart

@app.get("/get-quantity-categories-city-lomart")
def count_shop_by_categories_lomart(cityId : int="",cateId:int=""):
    responses = query_mongodb.count_shop_by_categorie_lomart(cityId= cityId,cateId=cateId)
    
    return {
        "quantity": responses
    }
 
# Shoppe

@app.get("/get-quantity-categories-city-shopee")
async def count_shop_by_categories_shopee(cityId : int="",cate:str=""):
    responses = query_mongodb.count_shop_by_categorie_shopee(cityId= cityId,cate=cate)
    
    return {
        "quantity": responses
    }   
# Liệt kê rating theo danh mục sản phẩm trong thành phố của shopee
@app.get("/get-list-shop-by-categories-city-shopee/{cityId}/{cate}/{k}")
def list_shop_by_categories_shopee(cityId : str="",cate:str="",k : int=""):
    responses = query_mongodb.list_rating_by_categories_in_city(cityId=cityId, cateId=cate,k=k)
    
    return {
        "quantity": responses
    }

# API liệt kê số lượt quan tâm theo danh mục sản phẩm trong thành phố (shopeefood)
@app.get("/sum-total-review-by-categories-city-shopee")
async def sum_review_by_categories_shopee(cityId : str="",cate:str=""):
    responses = await query_mongodb.sum_total_review_by_categories_in_city(cityId=cityId, cateId=cate)
    
    return {
        "quantity": responses
    }
# Hệ thống crawl dữ liệu theo thời gian
@app.get("/monitor-crawler-system") 
def monitor_crawler(collec_name, total_minute=60, step=5):
    ts_present=datetime.timestamp(datetime.now())
    response_collection_list = {}
    response_collection_list["time_series"] = [datetime.fromtimestamp(ts_present - step * 60).strftime(f"%Y-%m-%d %H:%M:%S") for step in range(0, int(total_minute), int(step))]
    response = query_mongodb.query_couting_fillter_collecs_by_time_series(
        collection_name=collec_name, 
        ts_present=ts_present, 
        interval_minutes = int(step), 
        interval_group_minutes = int(total_minute)
    )
    response["collection_name"] = collec_name
    response["desc"] = f"Query filter data format time series by collection {collec_name}, 10min per step in 60 min"
    response_collection_list[collec_name] = response
    return response_collection_list

# @app.on_event("startup")
# def welcome():
#     print("Web api is running on port 8000: http://127.0.0.1:8000")
    
if __name__ == "__main__":   
    # code here    
    count_shop_by_categories_lomart
    pass