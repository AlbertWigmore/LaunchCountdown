import json
import time
import requests
from pprint import pprint
from datetime import datetime, timedelta


class LaunchQuery:
    def __init__(self):
        self.url_base = 'https://launchlibrary.net/1.2/'

    def agency(self):
        pass

    def agencytype(self):
        pass

    def calendar(self):
        pass

    def eventtype(self):
        pass

    def launch(self, now, dur):
        current = now.strftime('%Y-%m-%d')
        next = (now + timedelta(days=dur)).strftime('%Y-%m-%d')
        r = requests.get(self.url_base + 'launch/' + current + '/' + next)
        return r.json()

    def launchevent(self):
        pass

    def launchstatus(self):
        pass

    def location(self):
        pass

    def mission(self):
        pass

    def missionevent(self):
        pass

    def missiontype(self):
        pass

    def pad(self):
        pass

    def rocket(self):
        pass

    def rocketevent(self):
        pass

    def rocketfamily(self):
        pass


if __name__ == '__main__':
    c = LaunchQuery()
    data = c.launch(datetime.now(), 7)
    for x in data['launches']:
        # pprint(x)
        print(x['name'])
        # print(x['rocket']['familyname'])
        print(x['rocket']['agencies'][0]['name'])
        print(x['location']['name'])
        print(x['net'])

        launch_time = datetime.strptime(x['net'], '%B %d, %Y %H:%M:%S UTC')
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
