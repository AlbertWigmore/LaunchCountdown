import time
from datetime import datetime

import LCDDriver
from LaunchQuery import LaunchQuery
from LCDInterface import LCDInterface

interface = LCDInterface()
interface.start()

c = LaunchQuery()


def acquire_launch():
    acquisition = True
    launch = 0
    while acquisition:
        data = c.launch_next(launch+1)
        launch_time = datetime.strptime(
            data['launches'][launch]['net'],
            '%B %d, %Y %H:%M:%S UTC'
        )
        if (launch_time - datetime.now()).total_seconds() < 0:
            acquisition = False
        else:
            launch += 1

    mission = data['launches'][launch]['missions'][0]['name']
    rocket = data['launches'][launch]['rocket']['name']
    location = data['launches'][launch]['location']['name']
    date = launch_time

    return (mission, rocket, location, date)


def run():
    mission, rocket, location, launch_time = acquire_launch()

    interface.write(
        [mission, rocket, location, ''],
        align=str.ljust
    )
    while True:
        time.sleep(0.01)
        s = (launch_time - datetime.now()).total_seconds()
        # if s < 0:
        days, remainder = [int(z) for z in divmod(s, 86400)]
        hours, remainder = [int(z) for z in divmod(remainder, 3600)]
        minutes, seconds = [int(z) for z in divmod(remainder, 60)]

        mention = '{:02} day(s) - {:02}:{:02}:{:02}'.format(days, hours, minutes, seconds)

        interface.write_line(3, mention, str.center)

    interface.stop()


if __name__ == '__main__':
    run()
