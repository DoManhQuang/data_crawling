import os, sys
import numpy as np
from datetime import datetime
ROOT = os.getcwd()
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from source.database.mongodb.mongodb import get_database
dbname = get_database()

def query_insert_many_data(collection_name, mylist):
    result = dict()
    try:
        status = dbname[collection_name].insert_many(mylist)
        result["inserted_ids"] = status.inserted_ids
        result["status"] = 1
    except Exception as err:
        result["mylist"] = mylist
        result["status"] = 0
        result["info"] = f"Unexpected {err=}, {type(err)=} - args: {err.args}"
    return result


def query_couting_fillter_collecs_by_time_series(collection_name, ts_present, interval_minutes = 10, interval_group_minutes = 60):
    pipeline = [
        {"$facet":{}}, 
        {"$project":{}},
        {"$project":{}}
    ]
    
    for step in range(0, interval_group_minutes, interval_minutes):
        time_query = ts_present - step * 60
        time_obj = datetime.fromtimestamp(time_query).strftime(f"%Y-%m-%d %H:%M:%S")
        pipeline[0]["$facet"].update({
            f"count_{step}": [
                {
                "$match": {
                    "create_time": {
                        "$gt": ts_present - (step + interval_minutes) * 60, 
                        "$lt": ts_present - step * 60}
                        }
                    }, 
                {"$count":"count"}]})
        
        pipeline[1]["$project"].update({
            f"count_{step}": { "$ifNull": [{ "$arrayElemAt": [f"$count_{step}.count", 0] }, 0] }
        })

        pipeline[2]["$project"].update({
            f'data_{step}': {
                'time': f"{time_obj}",
                'count': f"$count_{step}"
            }
        })
    results = list(dbname[collection_name].aggregate(pipeline))[0]
    return {
        "data": [results[name] for name in list(results)],
    }

def query_info_account(collection_name):
    results = list(dbname[collection_name].find({}, {"username": 1, "isBanned": 1, "timeBanned": 1, "_id": 0}))
    return {"data": results}


def query_cnt_fillter_domain_collecs_by_time_series(collection_name, ts_present, domains, interval_minutes = 10, interval_group_minutes = 60):
    response = {}
    for domain in domains:
        pipeline = [
            {"$facet":{}}, 
            {"$project":{}},
        ]
        for step in range(0, interval_group_minutes, interval_minutes):
            pipeline[0]["$facet"].update({
                f"{domain}_count_{step}": [
                    {
                    "$match": {
                        "domain": f"{domain}",
                        "create_time": {
                            "$gt": ts_present - (step + interval_minutes) * 60, 
                            "$lt": ts_present - step * 60}
                            }
                        }, 
                    {"$count":"count"}]})
            
            pipeline[1]["$project"].update({
                f"{domain}_count_{step}": { "$ifNull": [{ "$arrayElemAt": [f"${domain}_count_{step}.count", 0] }, 0] }
            })

        results_domain = list(dbname[collection_name].aggregate(pipeline))[0]
        response[f"{domain}"] = [results_domain[name] for name in list(results_domain)]
    
    response["Total"] = np.zeros(len(response[domains[0]]), dtype=int)
    for domain in domains:
        response["Total"] += response[domain]
    response["Total"] = response["Total"].tolist()
    return {
        "data": response,
    }


def count_all_data_unique_v2(collection_name, domains):

    pipeline = [
            {"$facet":{}}, 
            {"$project":{}},
            {"$project":{
                "total_count": {"$sum": []}
            }},
        ]

    for domain in domains:
        pipeline[0]["$facet"].update({
            f"{domain}_count":[
                {"$match": {"domain": f"{domain}"}},
                {"$count":"count"}
            ]
        })

        pipeline[1]["$project"].update({
            f"{domain}":{
                "$ifNull": [{ "$arrayElemAt": [f"${domain}_count.count", 0] }, 0]
            }
        })

        pipeline[2]["$project"].update({
            f"{domain}_count": f"${domain}"
        })

        pipeline[2]["$project"]["total_count"]["$sum"].append(f"${domain}")
    return list(dbname[collection_name].aggregate(pipeline))[0]


def count_new_data_unique_v2(collection_name, domains, ts_present, minutes=5):

    pipeline = [
            {"$facet":{}}, 
            {"$project":{}},
            {"$project":{
                "total_count": {"$sum": []}
            }},
        ]
    
    for domain in domains:
        pipeline[0]["$facet"].update({
            f"{domain}_count":[
                {"$match": {
                    "domain": f"{domain}",
                    "create_time": {"$gt": ts_present - minutes*60, "$lt": ts_present}
                    }
                },
                {"$count":"count"}
            ]
        })

        pipeline[1]["$project"].update({
            f"{domain}":{
                "$ifNull": [{ "$arrayElemAt": [f"${domain}_count.count", 0] }, 0]
            }
        })

        pipeline[2]["$project"].update({
            f"{domain}_count": f"${domain}"
        })

        pipeline[2]["$project"]["total_count"]["$sum"].append(f"${domain}")
    return list(dbname[collection_name].aggregate(pipeline))[0]


def tbl_grabfood_group_by_location(collection_name):
    pipeline = [
        {
            "$group": {
                "_id": {
                    "poiID":"$poiID",
                    "location": "$location"
                }
            }
        }
    ]
    return list(dbname[collection_name].aggregate(pipeline))


if __name__ == "__main__":   
    # code here
    pass
