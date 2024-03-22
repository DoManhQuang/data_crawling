import os, sys, time
import datetime


ROOT = os.getcwd()
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
    
from source.ecom_api.shopee_food import call_api_get_info_shop_use_res_ids

     

def background_task():
    timeDelay = 5 # 5 phút chạy 1 lần
    while True:
        print("Updating time: " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        call_api_get_info_shop_use_res_ids(collection_name="shopefood_6_6_t2",
                                       token="17fcb31a031f94c1ff5a79f8b3488d30e80e9b9f28c9730d4b6e2b58cc5d4b3d7585b37fc1a2d454b9f5890809d8dc0fe2289d953eca5f4bbdc0afb6b73b2d1e")
        time.sleep(timeDelay)


if __name__ == "__main__":   
    # code here   
    background_task() 
    pass