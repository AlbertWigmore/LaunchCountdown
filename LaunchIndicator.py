import signal
import gi
import time
from datetime import datetime, timedelta
from LaunchQuery import LaunchQuery, update_launch_countdown
from threading import Thread
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GObject


class Indicator():
    def __init__(self):
        self.app = 'LaunchIndicator'
        iconpath = "/home/alb/Documents/rocket1.png"
        self.indicator = AppIndicator3.Indicator.new(
            self.app, iconpath,
            AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        self.indicator.set_label("Launch", self.app)
        self.update = Thread(target=self.show_launch)
        self.update.setDaemon(True)
        self.update.start()

    def create_menu(self):
        menu = Gtk.Menu()
        c = LaunchQuery()
        data = c.launch_next_full(5)
        for x in data['launches']:
            launchname = Gtk.MenuItem(x['name'])
            menu.append(launchname)
            launchtime = Gtk.MenuItem(x['net'])
            menu.append(launchtime)
            launchlocation = Gtk.MenuItem(x['location']['name'])
            menu.append(launchlocation)
            menu_sep = Gtk.SeparatorMenuItem()
            menu.append(menu_sep)
        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', self.stop)
        menu.append(item_quit)

        menu.show_all()
        return menu

    def show_launch(self):
        c = LaunchQuery()
        data = c.launch(next=1)
        launch_time = datetime.strptime(data['launches'][0]['net'], '%B %d, %Y %H:%M:%S UTC')
        while True:
            s = (launch_time - datetime.now()).total_seconds()
            days, remainder = [int(z) for z in divmod(s, 86400)]
            hours, remainder = [int(z) for z in divmod(remainder, 3600)]
            minutes, seconds = [int(z) for z in divmod(remainder, 60)]
            time.sleep(1)
            mention = str(days) + ' days, ' + str(hours) + ':' + str(minutes) + ':' + str(seconds)
            GObject.idle_add(
                self.indicator.set_label,
                mention, self.app,
                priority=GObject.PRIORITY_DEFAULT
                )

    def stop(self, source):
        Gtk.main_quit()


Indicator()
# this is where we call GObject.threads_init()
GObject.threads_init()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
