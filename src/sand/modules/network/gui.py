import cairo
import gi
import threading
import time

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository.GdkPixbuf import Pixbuf, InterpType

from sand.gui_module import GUIComponent
from sand.modules.network.sensor import NetworkDevices, NetworkDeviceIO
import os
import pkg_resources


class SandNetworkGui(GUIComponent):
    def __init__(self, configuration="configuration.yaml"):
        GUIComponent.__init__(self, "{}/{}".format(__package__, configuration))
        self._network_devices = NetworkDevices()
        self._network_devices.read()
        self._network_io = NetworkDeviceIO(self._network_devices.data)
        self._memory_information = None

        self.current_drawing_offset = self.configuration["start-drawing-offset"]
        self._module_color = "#{}".format(self.configuration["module-color"])
        self._thread_refresh = None

    def create_icon(self):
        label_description = Gtk.Label()
        label_description.set_markup("<span foreground='{}'><i><big><b>{}</b></big></i></span>".format(self._module_color, self.configuration["description"]))
        self.layout.put(label_description, self.configuration["description-position-x"], self.configuration["description-position-y"])

        image = Gtk.Image()
        icon_filepath = pkg_resources.resource_filename(__name__, self.configuration["icon-filename"])
        pixbuf = Pixbuf.new_from_file(icon_filepath)
        image.set_from_pixbuf(pixbuf.scale_simple(self.configuration["icon-dimension-x"],
                                                  self.configuration["icon-dimension-y"], InterpType.BILINEAR))
        self.layout.put(image, self.configuration["icon-position-x"], self.configuration["icon-position-y"])

    def build(self):
        self.create_icon()
        #self._build_memory_labels()
        self._thread_refresh = threading.Thread(target=self.refresh, args=())
        self._thread_refresh.setDaemon(True)
        self._thread_refresh.start()

    def _build_memory_labels(self):
        pass

    def refresh(self):
        while True:
            time.sleep(self.configuration["refresh-time"])

