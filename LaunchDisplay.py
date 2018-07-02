import LCDDriver
import time
from datetime import datetime
from LaunchQuery import LaunchQuery
from LCDInterface import LCDInterface

interface = LCDInterface()
interface.start()
try:
    c = LaunchQuery()
    data = c.launch_next_full(1)

    interface.write([data['launches'][0]['missions'][0]['name'].encode('ASCII'),
                     data['launches'][0]['rocket']['name'].encode('ASCII'),
                     data['launches'][0]['location']['name'].encode('ASCII'),
                     ''], align=str.ljust)

    launch_time = datetime.strptime(data['launches'][0]['net'], '%B %d, %Y %H:%M:%S UTC')
    while True:
        time.sleep(0.01)
        s = (launch_time - datetime.now()).total_seconds()
        # if s < 0:
        days, remainder = [int(z) for z in divmod(s, 86400)]
        hours, remainder = [int(z) for z in divmod(remainder, 3600)]
        minutes, seconds = [int(z) for z in divmod(remainder, 60)]

        mention = '{:02} day(s) - {:02}:{:02}:{:02}'.format(days, hours, minutes, seconds)

        interface.write_line(3, mention, str.center)
finally:
    interface.stop()
