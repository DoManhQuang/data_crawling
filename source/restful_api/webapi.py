from fastapi import FastAPI, Query
import os, sys
from datetime import datetime, timezone

ROOT = os.getcwd()
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
    
import source.database.mongodb.query_mongodb as query_mongodb
app = FastAPI()

@app.get("/")
def ping():
    return{
        "hello": "world"
    }

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

@app.get("/get-quantity-shopee") 
def count_shopee_food(location: str = ""):
    responses = query_mongodb.count_shopee(location_url= location)
    
    return {
        "quantity": responses
    }

@app.get("/get-quantity-lomart") 
def count_lomarts(category: str = ""):
    responses = query_mongodb.count_lomart(category= category)
    
    return {
        "quantity": responses
    }

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
    
# if __name__ == "__main__":   
#     # code here    
#     print("Web api start.")
#     pass