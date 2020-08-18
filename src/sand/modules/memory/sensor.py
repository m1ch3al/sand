from sand.sensor_module import HardwareSensorModule
import subprocess
import os
import glob


class MemorySensor(HardwareSensorModule):
    def __init__(self):
        HardwareSensorModule.__init__(self)
        self._process = None
        self._information = dict()
        self._information["total"] = 0
        self._information["free"] = 0
        self._information["used"] = 0
        self._information["cached"] = 0
        self._information["swap-total"] = 0
        self._information["swap-free"] = 0
        self._information["swap-used"] = 0

    def run_command(self):
        self._process = subprocess.Popen(["cat", "/proc/meminfo"], stdout=subprocess.PIPE)
        data_from_command = self._process.communicate()[0].decode()
        splitted = data_from_command.split("\n")
        for element in splitted:
            if element.startswith("MemTotal"):
                value = int(element.replace("MemTotal:", "").replace("kB", "").replace(" ", ""))
                self._information["total"] = round((value/(1024*1024)), 2)
            if element.startswith("MemFree"):
                value = int(element.replace("MemFree:", "").replace("kB", "").replace(" ", ""))
                self._information["free"] = round((value/(1024*1024)), 2)
                self._information["used"] = round((self._information["total"] - self._information["free"]), 2)
            if element.startswith("Cached"):
                value = int(element.replace("Cached:", "").replace("kB", "").replace(" ", ""))
                self._information["cached"] = round((value/(1024*1024)), 2)
            if element.startswith("SwapTotal"):
                value = int(element.replace("SwapTotal:", "").replace("kB", "").replace(" ", ""))
                self._information["swap-total"] = round((value/(1024*1024)), 2)
            if element.startswith("SwapFree"):
                value = int(element.replace("SwapFree:", "").replace("kB", "").replace(" ", ""))
                self._information["swap-free"] = round((value/(1024*1024)), 2)
                self._information["swap-used"] = round((self._information["swap-total"] - self._information["swap-free"]), 2)
        self.data = self._information

def main():
    c = MemorySensor()
    print(c.read())


if __name__ == "__main__":
    main()