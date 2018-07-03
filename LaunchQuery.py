import requests


class LaunchQuery(object):
    def __init__(self, *args, **kwargs):
        self.version = '1.4'
        self.url_base = 'https://launchlibrary.net/' + self.version + '/'

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

    def launch_next(self, next):
        r = requests.get(self.url_base + 'launch/next/' + str(next))
        return r.json()
