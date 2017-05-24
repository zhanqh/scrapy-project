import requests
import redis
from requests.exceptions import RequestException

def main():
    try:
        response = requests.get('http://dev.kuaidaili.com/api/getproxy/?orderid=969779508725175&num=200&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=1&an_ha=1&sp1=1&sp2=1&sep=%2C')
        if response.status_code is 200:
            result = response.text
    except RequestException:
        print('请求异常')

    proxies = result.split(',')

    db = redis.Redis(host='127.0.0.1', port='6379')

    if db.keys('proxy:1:*'):
        for proxy in proxies:
            db.set('proxy:2:'+proxy, proxy)
        print('向 proxy:2 插入' + str(len(proxies)) + ' 个代理')
        print('删除 proxy:1 中的 ' + str(len(db.keys('proxy:1:*'))) + ' 个代理')
        for key in db.keys('proxy:1:*'):
            db.delete((key).decode('ascii'))
    else:
        for proxy in proxies:
            db.set('proxy:1:'+proxy, proxy)
        print('向 proxy:1 插入' + str(len(proxies)) + ' 个代理')
        print('删除 proxy:2 中的 ' + str(len(db.keys('proxy:2:*'))) + ' 个代理')
        for key in db.keys('proxy:2:*'):
            db.delete((key).decode('ascii'))


if __name__ == '__main__':
    main()
