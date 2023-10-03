import redis

r = redis.Redis(host='localhost', port=6379, db=0)

r.set('123', 'question')

print(r.get('123'))