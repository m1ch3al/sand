from sand.modules.sensor_module import HardwareSensorModule
import subprocess


class NetworkDevices(HardwareSensorModule):
    def __init__(self):
        HardwareSensorModule.__init__(self)
        self._process = None

    def run_command(self):
        self._process = subprocess.Popen(["ip", "address"], stdout=subprocess.PIPE)
        data_from_command = self._process.communicate()[0].decode()
        self._process.stdout.close()
        splitted = data_from_command.split("\n")
        self.data = dict()
        for element in splitted:
            try:
                int(element[0])
                values = element.split(" ")
                interface_name = values[1].replace(":", "").replace(" ", "")
                if "lo" not in interface_name:
                    self.data[interface_name] = None
                    if "NO-CARRIER" in element:
                        self.data[interface_name] = "disconnected"
                    else:
                        self.data[interface_name] = self._get_interface_ip_address(interface_name)
            except Exception as ex:
                pass

    def _get_interface_ip_address(self, interface_name):
        primary_process = subprocess.Popen(["ifconfig", interface_name], stdout=subprocess.PIPE)
        pipe_process = subprocess.Popen(["grep", "inet "], stdin=primary_process.stdout, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        primary_process.stdout.close()
        data_from_command = pipe_process.communicate()[0].decode()
        pipe_process.stdout.close()
        splitted = data_from_command.split(" ")
        for i in range(0, len(splitted)):
            if "inet" in splitted[i]:
                return splitted[i+1]


class NetworkDeviceIO(NetworkDevices):
    def __init__(self, devices):
        HardwareSensorModule.__init__(self)
        self._process = None
        self._devices = devices
        self._create_structure()

    def _create_structure(self):
        for device_name in self._devices:
            status = self._devices[device_name]
            self._devices[device_name] = dict()
            self._devices[device_name]["status"] = status
            self._devices[device_name]["received_bytes"] = None
            self._devices[device_name]["received_packets"] = None
            self._devices[device_name]["transmitted_bytes"] = None
            self._devices[device_name]["transmitted_packets"] = None

    def run_command(self):
        self._process = subprocess.Popen(["cat", "/proc/net/dev"], stdout=subprocess.PIPE)
        data_from_command = self._process.communicate()[0].decode()
        splitted = data_from_command.split("\n")
        for device_name in self._devices:
            for line in splitted:
                if line.startswith(device_name):
                    splitted_data = line.split(" ")
                    self._set_data(device_name, splitted_data)
        self._process.stdout.close()
        self.data = self._devices

    def _set_data(self, device_name, data):
        if "disconnected" in self._devices[device_name]["status"]:
            self._devices[device_name]["received_bytes"] = 0
            self._devices[device_name]["received_packets"] = 0
            self._devices[device_name]["transmitted_bytes"] = 0
            self._devices[device_name]["transmitted_packets"] = 0
        else:
            self._devices[device_name]["received_bytes"] = int(data[1])
            self._devices[device_name]["received_packets"] = int(data[3])
            self._devices[device_name]["transmitted_bytes"] = int(data[40])
            self._devices[device_name]["transmitted_packets"] = int(data[42])

import time

if __name__ == "__main__":
    c = NetworkDevices()
    print(c.read())

    d = NetworkDeviceIO(c.data)
    while True:
        data = d.read()
        print(data["wlp2s0"])
        time.sleep(1)