import cairo
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk
from gi.repository import Gdk

import importlib

from sand.modules.cpu.gui import SandCPUGui
from sand.modules.memory.gui import SandMemoryGui


class TransparentWindow(Gtk.Window):
    """ A transparent and borderless window, fixed on the desktop."""

    def __init__(self, configuration):
        Gtk.Window.__init__(self)
        self._configuration = configuration
        self.modules = dict()

        self.layout = Gtk.Fixed()
        self.add(self.layout)
        self._counter = 0
        self.set_size_request(self._configuration["widget-width"], self._configuration["widget-height"])
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)
        self.set_keep_below(True)
        self.set_decorated(False)
        self.stick()

        self.connect('destroy', Gtk.main_quit)
        self.connect('draw', self.draw)

        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)

        self.set_app_paintable(True)
        self.move(self._configuration["widget-position-x"], self._configuration["widget-position-y"])

        self.build_modules()

    def draw(self, widget, context):
        context.set_source_rgba(255, 255, 255, 0)
        context.set_operator(cairo.OPERATOR_SOURCE)
        context.paint()
        context.set_operator(cairo.OPERATOR_OVER)

    def build_modules(self):
        for element in self._configuration["sand-modules-to-load"]:
            module_name = element["module"]["module-name"]
            class_name = element["module"]["class-name"]
            position_x = element["module"]["position-x"]
            position_y = element["module"]["position-y"]

            sand_module = instantiate_class(class_name, module_name, [])
            sand_module.build()
            self.layout.put(sand_module.get_gui(), position_x, position_y)


def instantiate_class(class_name, module_name, constructor_parameters):
    try:
        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)
        class_instantiated = class_(*constructor_parameters)
        return class_instantiated
    except Exception as ex:
        message = "Introspection Exception : try to create this class [{}] in this module : [{}]".format(class_name, module_name)
        message += "Cannot instantiate the requested object class : {}".format(ex)
        raise Exception(message)




def main():
    window = TransparentWindow()
    window.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()