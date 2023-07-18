import redis

def get_redis(db=2):
    r = redis.Redis(
        host="localhost", port=6379,
        username="ecom_mining_dev", # use your Redis user. More info https://redis.io/docs/management/security/acl/
        password="Ec0mM1ningDev", # use your Redis password
        db=db
    )
    return r

def test(r):
    data = {}
    queue_names = r.keys('*')
    # Print the queue names
    for queue_name in queue_names:
        # print(queue_name.decode())
        # Get the length (count) of the queue
        queue_length = r.llen(queue_name.decode())
        # print(f"Queue length: {queue_length}")
        data[queue_name.decode()] = queue_length

    print(data)
if __name__ == '__main__':
    test(get_redis(9))