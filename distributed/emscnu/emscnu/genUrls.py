import redis

conn = redis.ConnectionPool(host='127.0.0.1', port='6379')
r = redis.Redis(connection_pool=conn)

urls = ['http://em.scnu.edu.cn/xueyuantongzhi/'+str(x)+'.html' for x in range(2,145)]

r.lpush('myspider:start_urls', *urls)
