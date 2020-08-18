from abc import ABC, abstractmethod

import gi
import yaml

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import pkg_resources
import os


class GUIComponent(ABC):
    def __init__(self, configuration_file_path):
        super().__init__()
        splitted = configuration_file_path.split("/")
        package_file_path = splitted[0].replace(".", "/").replace("sand", "")
        package_file_path = os.path.join(package_file_path, splitted[1])
        self.configuration_filepath = pkg_resources.resource_filename(__name__, package_file_path)
        self.configuration = read_yaml_configuration_file(self.configuration_filepath)
        self.layout = Gtk.Fixed()

    @abstractmethod
    def create_icon(self):
        pass

    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def refresh(self):
        pass

    def get_gui(self):
        return self.layout


def read_yaml_configuration_file(configuration_filepath):
    with open(configuration_filepath, "r") as fd:
        configuration = yaml.safe_load(fd)
    fd.close()
    return configuration