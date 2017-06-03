import json
import time
import requests
from pprint import pprint
from datetime import datetime, timedelta


class LaunchQuery:
    def __init__(self):
        self.url_base = 'https://launchlibrary.net/1.1/'

    def launches(self, now, dur):
        current = now.strftime('%Y-%m-%d')
        next = (now + timedelta(days=dur)).strftime('%Y-%m-%d')
        r = requests.get(self.url_base + 'launch/' + current + '/' + next)

        return r.json()

if __name__ == '__main__':
    c = LaunchQuery()
    data = c.launches(datetime.now(), 7)
    for x in data['launches']:
        print(x['name'])

        launch_time = datetime.strptime(x['net'], '%B %d, %Y %H:%M:%S UTC')
        x = True
        while x:
            s = (launch_time - datetime.now()).total_seconds()
            if s < 0:
                print('Launch!')
                x = False
                continue
            days, remainder = [int(z) for z in divmod(s, 86400)]
            hours, remainder = [int(z) for z in divmod(remainder, 3600)]
            minutes, seconds = [int(z) for z in divmod(remainder, 60)]
            print '\r' + str(days) + ' days, ' + str(hours) + ':' + \
                  str(minutes) + ':' + str(seconds),
            time.sleep(1)
