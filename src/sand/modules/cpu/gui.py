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
from sand.modules.cpu.sensor import CPUType, CPUCoreFrequencies, CPUVendor, CPUCoreTemperature
import os
import pkg_resources


class SandCPUGui(GUIComponent):
    def __init__(self, configuration="configuration.yaml"):
        GUIComponent.__init__(self, "{}/{}".format(__package__, configuration))
        self._cores = []
        self._temps = []
        self._label_cores = []
        self._cpu_frequencies = CPUCoreFrequencies()
        self._cpu_temperatures = CPUCoreTemperature()
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

        label = Gtk.Label()
        label.set_markup("<span foreground='{}'>CPU Vendor:</span>".format(self._module_color))
        self.layout.put(label, 0, self.current_drawing_offset)
        cpu_vendor = CPUVendor()
        label_cpu_vendor = Gtk.Label()
        label_cpu_vendor.set_markup("<span foreground='{}'><b>{}</b></span>".format(self._module_color, cpu_vendor.read()))
        self.layout.put(label_cpu_vendor, 80, self.current_drawing_offset)

        self.current_drawing_offset += self.configuration["horizontal-spacing"]

        label = Gtk.Label()
        label.set_markup("<span foreground='{}'>CPU Type:</span>".format(self._module_color))
        self.layout.put(label, 0, self.current_drawing_offset)
        cpu_type = CPUType()
        label_cpu_type = Gtk.Label()
        label_cpu_type.set_markup("<span foreground='{}'><b>{}</b></span>".format(self._module_color, cpu_type.read()))
        self.layout.put(label_cpu_type, 70, self.current_drawing_offset)

        self._build_cores_labels()

        self._thread_refresh = threading.Thread(target=self.refresh, args=())
        self._thread_refresh.setDaemon(True)
        self._thread_refresh.start()

    def _build_cores_labels(self):
        self.current_drawing_offset += self.configuration["horizontal-spacing"]
        self._cores = self._cpu_frequencies.read()
        self._temps = self._cpu_temperatures.read()
        label = Gtk.Label()
        label.set_markup("<span foreground='{}'>Total number of core(s): <b>{}</b></span>".format(self._module_color, len(self._temps)))
        self.layout.put(label, 0, self.current_drawing_offset)
        core_counter = 0
        self.current_drawing_offset += self.configuration["horizontal-spacing"]
        for single_core in self._temps:
            label = Gtk.Label()
            label.set_markup("<span foreground='{}'>Core ID #{}: <b>{} Mhz</b> - Temp: <b>{} °C</b></span>".format(self._module_color, core_counter, self._cores[core_counter], self._temps[single_core]))
            core_counter += 1
            self._label_cores.append(label)
            self.layout.put(label, 0, self.current_drawing_offset)
            self.current_drawing_offset += self.configuration["horizontal-spacing"]

    def refresh(self):
        while True:
            self._cores = self._cpu_frequencies.read()
            self._temps = self._cpu_temperatures.read()
            i = 0
            for single_core in self._temps:
                self._label_cores[i].set_markup("<span foreground='{}'>Core ID #{}: <b>{} Mhz</b> - Temp: <b>{} °C</b></span>".format(self._module_color, single_core, self._cores[single_core], self._temps[single_core]))
                i += 1
            time.sleep(self.configuration["refresh-time"])



