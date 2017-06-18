import LCDDriver
import time
from datetime import datetime
from LaunchQuery import LaunchQuery

lcd = LCDDriver.lcd()

lcd.lcd_clear()

c = LaunchQuery()
data = c.launch_next_full(1)

lcd.lcd_display_string(data['launches'][0]['missions'][0]['name'], 1)
lcd.lcd_display_string(data['launches'][0]['rocket']['name'], 2)
lcd.lcd_display_string(data['launches'][0]['location']['name'], 3)

launch_time = datetime.strptime(data['launches'][0]['net'], '%B %d, %Y %H:%M:%S UTC')
while True:
    time.sleep(0.5)
    s = (launch_time - datetime.now()).total_seconds()
    # if s < 0:
    days, remainder = [int(z) for z in divmod(s, 86400)]
    hours, remainder = [int(z) for z in divmod(remainder, 3600)]
    minutes, seconds = [int(z) for z in divmod(remainder, 60)]

    mention = '  ' + str(days) + ' days, ' + str(hours) + ':' + str(minutes) + ':' + str(seconds)

    lcd.lcd_display_string(mention, 4)
