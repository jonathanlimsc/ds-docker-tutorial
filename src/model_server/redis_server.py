import redis

class RedisServer():
    def __init__(self, host, port, db):
        # Initialise Redis server connection
        self.db = redis.StrictRedis(host=host, port=port, db=db)

    def key_exists(self, key):
        occurences = self.db.exists(key)
        return True if occurences > 0 else False

    def get_keys(self, pattern='*'):
        return self.db.keys(pattern=pattern)

    def set(self, key, value, expiry=None):
        self.db.set(key, value, ex=expiry)

    def get(self, key):
        return self.db.get(key)

    def delete(self, key):
        if self.key_exists(key):
            self.db.delete(key)

    def get_queue_length(self, queue_name):
        return self.db.llen(queue_name)

    def enqueue(self, queue_name, value):
        self.db.rpush(queue_name, value)

    def dequeue(self, queue_name, timeout=0):
        # length = self.db.llen(queue_name)
        # return self.db.lpop(queue_name) if length > 0 else None
        return self.db.blpop(queue_name, timeout=timeout)[1]

    def get_list_element_by_index(self, list_name, index):
        length = self.db.llen(list_name)
        return self.db.lindex(list_name, index) if length > 0 and index < length else None

    def flushall(self):
        self.db.flushall()

if __name__ == '__main__':
    import json
    import config

    # Tests

    redis = RedisServer(host=config.REDIS_HOST,
            port=config.REDIS_PORT, db=config.REDIS_DB)

    redis.set('first_key',json.dumps({'prediction': 3}))
    print(redis.get('first_key'))

    redis.enqueue('queue', json.dumps({'job_id':1012121324, 'image': 'Awsesaldk23920sd'}))
    redis.enqueue('queue', json.dumps({'job_id':1012121325, 'image': 'Bwsesaldk23920sd'}))
    redis.enqueue('queue', json.dumps({'job_id':1012121326, 'image': 'Cwsesaldk23920sd'}))
    assert redis.get_queue_length('queue') == 3, "Queue is not length 3"

    job = redis.dequeue('queue')
    print(job)
    job_obj = json.loads(job.decode('utf-8'))
    print(job_obj)
    assert redis.get_queue_length('queue') == 2, "Queue is not length 2"

    print(redis.dequeue('queue'))
    assert redis.get_queue_length('queue') == 1, "Queue is not length 1"

    print(redis.dequeue('queue'))
    assert redis.get_queue_length('queue') == 0, "Queue is not length 0"

    print(redis.get_keys())
    assert len(redis.get_keys()) == 1, "Number of keys is not 1"

    redis.flushall()

    assert len(redis.get_keys()) == 0, "Number of keys is not 0"
