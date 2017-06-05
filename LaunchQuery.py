import json
import time
import requests
from pprint import pprint
from datetime import datetime, timedelta


class LaunchQuery(object):
    def __init__(self, *args, **kwargs):
        self.url_base = 'https://launchlibrary.net/1.2/'

    def __getattr__(self, method_name):
        if method_name in ['agency', 'agencytype', 'calendar', 'eventtype',
                           'launch', 'launchevent', 'launchstatus', 'location',
                           'mission', 'missionevent', 'missiontype', 'pad',
                           'rocket', 'rocketevent', 'rocketfamily']:
            def get(*args, **kwargs):
                r = requests.get(self.url_base + method_name, params=kwargs)
                return r.json()
            return get
        else:
            raise AttributeError()

    def launch2(self, now, dur):
        current = now.strftime('%Y-%m-%d')
        next = (now + timedelta(days=dur)).strftime('%Y-%m-%d')
        r = requests.get(self.url_base + 'launch/' + current + '/' + next)
        return r.json()


if __name__ == '__main__':
    c = LaunchQuery()
    data = c.launch(next=1)
    launch_time = datetime.strptime(data['launches'][0]['net'], '%B %d, %Y %H:%M:%S UTC')
    print(launch_time)
    x = True
    while x:
        s = (launch_time - datetime.now()).total_seconds()
        if s < 0:
            x = False
            continue
        days, remainder = [int(z) for z in divmod(s, 86400)]
        hours, remainder = [int(z) for z in divmod(remainder, 3600)]
        minutes, seconds = [int(z) for z in divmod(remainder, 60)]
        print '\r' + str(days) + ' days, ' + str(hours) + ':' + str(minutes) + ':' + str(seconds)
        time.sleep(1)
