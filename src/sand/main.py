import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sand.dock_main import TransparentWindow
from sand.gui_module import read_yaml_configuration_file
import os


def main():
    homedir = os.path.expanduser("~")
    sand_configuration_folder = os.path.join(homedir, ".sand")
    configuration_filepath = os.path.join(sand_configuration_folder, "configuration.yaml")
    configuration = read_yaml_configuration_file(configuration_filepath)

    window = TransparentWindow(configuration)
    window.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
