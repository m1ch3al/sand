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

        stat_script = pkg_resources.resource_filename(__name__, self.configuration["statistics-script"])
        self._network_io = NetworkDeviceIO(self._network_devices.data, stat_script)
        self._labels_interfaces_status = dict()
        self._images_interfaces_status = dict()
        for interface in self.configuration["interfaces"]["ethernet"]:
            self._labels_interfaces_status[interface] = None
            self._images_interfaces_status[interface] = None

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
        self._build_ethernet_gui()
        self._build_wifi_gui()
        self._thread_refresh = threading.Thread(target=self.refresh, args=())
        self._thread_refresh.setDaemon(True)
        self._thread_refresh.start()

    def _build_ethernet_gui(self):
        system_devices = self._network_devices.read()
        for interface in self.configuration["interfaces"]["ethernet"]:
            if interface in system_devices:
                status = system_devices[interface]
                label = Gtk.Label()
                self._set_ethernet_status(interface, status)
                if "disconnected" in status.lower():
                    label.set_markup("<span foreground='{}'><i><b>{} :  </b></i></span><span foreground='#{}'><b>{}</b></span>".format(self._module_color, interface, self.configuration["disconnection-color"], status))
                else:
                    label.set_markup("<span foreground='{}'><i><b>{} :  </b></i><b>{}</b></span>".format(self._module_color, interface, status))
                self.layout.put(label, self.configuration["left-padding-interface-status"]+self.configuration["interface-status-dimension-x"]+5, self.current_drawing_offset + int(self.configuration["interface-status-dimension-y"]/6))
                self.current_drawing_offset += self.configuration["horizontal-spacing"]
                self.current_drawing_offset += self.configuration["interface-status-dimension-x"]-10
                self._labels_interfaces_status[interface] = label

    def _set_ethernet_status(self, inteface, status):
        image = Gtk.Image()
        if "disconnected" in status.lower():
            icon_filepath = pkg_resources.resource_filename(__name__, self.configuration["ethernet-down-icon-filename"])
        else:
            icon_filepath = pkg_resources.resource_filename(__name__, self.configuration["ethernet-up-icon-filename"])
        pixbuf = Pixbuf.new_from_file(icon_filepath)
        image.set_from_pixbuf(pixbuf.scale_simple(self.configuration["interface-status-dimension-x"],
                                                  self.configuration["interface-status-dimension-y"], InterpType.BILINEAR))
        self.layout.put(image, self.configuration["left-padding-interface-status"], self.current_drawing_offset)
        self._images_interfaces_status[inteface] = image

    def _set_wifi_status(self, inteface, status):
        image = Gtk.Image()
        if "disconnected" in status.lower():
            icon_filepath = pkg_resources.resource_filename(__name__, self.configuration["wifi-down-icon-filename"])
        else:
            icon_filepath = pkg_resources.resource_filename(__name__, self.configuration["wifi-up-icon-filename"])
        pixbuf = Pixbuf.new_from_file(icon_filepath)
        image.set_from_pixbuf(pixbuf.scale_simple(self.configuration["interface-status-dimension-x"],
                                                  self.configuration["interface-status-dimension-y"], InterpType.BILINEAR))
        self.layout.put(image, self.configuration["left-padding-interface-status"], self.current_drawing_offset)
        self._images_interfaces_status[inteface] = image

    def _build_wifi_gui(self):
        system_devices = self._network_devices.read()
        for interface in self.configuration["interfaces"]["wifi"]:
            if interface in system_devices:
                status = system_devices[interface]
                label = Gtk.Label()
                self._set_wifi_status(interface, status)
                if "disconnected" in status.lower():
                    label.set_markup("<span foreground='{}'><i><b>{} :  </b></i></span><span foreground='#0003d1'><b>{}</b></span>".format(self._module_color, interface, status))
                else:
                    label.set_markup("<span foreground='{}'><i><b>{} :  </b></i><b>{}</b></span>".format(self._module_color, interface, status))
                self.layout.put(label, self.configuration["left-padding-interface-status"]+self.configuration["interface-status-dimension-x"]+5, self.current_drawing_offset + int(self.configuration["interface-status-dimension-y"]/6))
                self.current_drawing_offset += self.configuration["horizontal-spacing"]
                self.current_drawing_offset += self.configuration["interface-status-dimension-x"]-10
                self._labels_interfaces_status[interface] = label

    def refresh(self):
        while True:
            time.sleep(self.configuration["refresh-time"])

