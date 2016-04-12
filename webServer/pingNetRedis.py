def pingNet():
    import redis
    import time
    import sys
    import os
    import json

    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    with open('ip_devices.json') as data_file:
        devices = json.load(data_file)

    for name in devices:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        if os.system("ping -c 1 -W 1 " + devices[name]) == 0:
            r.set('ping.' + name + '.status', 'up')
        else:
            r.set('ping.' + name + '.status', 'down')
        r.set('ping.' + name + '.timestamp', timestamp)

if __name__ == "__main__":
    pingNet()
