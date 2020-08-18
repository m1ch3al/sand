from sand.sensor_module import HardwareSensorModule
import subprocess
import os
import glob


class CPUType(HardwareSensorModule):
    def __init__(self):
        HardwareSensorModule.__init__(self)
        self._process = None

    def run_command(self):
        self._process = subprocess.Popen(["cat", "/proc/cpuinfo"], stdout=subprocess.PIPE)
        pipe_process = subprocess.Popen(["grep", "model name"], stdin=self._process.stdout, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        self._process.stdout.close()
        data_from_command = pipe_process.communicate()[0].decode()
        splitted = data_from_command.split("\n")
        self.data = splitted[0].replace("model name\t: ", "")
        pipe_process.stdout.close()


class CPUVendor(HardwareSensorModule):
    def __init__(self):
        HardwareSensorModule.__init__(self)
        self._process = None

    def run_command(self):
        self._process = subprocess.Popen(["cat", "/proc/cpuinfo"], stdout=subprocess.PIPE)
        pipe_process = subprocess.Popen(["grep", "vendor_id"], stdin=self._process.stdout, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        self._process.stdout.close()
        data_from_command = pipe_process.communicate()[0].decode()
        splitted = data_from_command.split("\n")
        self.data = splitted[0].replace("vendor_id\t: ", "")
        pipe_process.stdout.close()


class CPUCoreFrequencies(HardwareSensorModule):
    def __init__(self):
        HardwareSensorModule.__init__(self)
        self._process = None

    def run_command(self):
        self._process = subprocess.Popen(["cat", "/proc/cpuinfo"], stdout=subprocess.PIPE)
        pipe_process = subprocess.Popen(["grep", "cpu MHz"], stdin=self._process.stdout, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        self._process.stdout.close()
        data_from_command = pipe_process.communicate()[0].decode()
        pipe_process.stdout.close()
        splitted = data_from_command.split("\n")
        self.data = []
        for element in splitted:
            frequency = element.replace("cpu MHz\t\t: ", "")
            if len(frequency) > 0:
                self.data.append(frequency)


class CPUCoreTemperature(HardwareSensorModule):
    def __init__(self):
        HardwareSensorModule.__init__(self)
        self._process = None

    def run_command(self):
        thermal_directory = "/sys/class/thermal/thermal_zone*"
        result = glob.glob(thermal_directory)
        counter = 0
        thermal_data = dict()
        for element in result:
            self._process = subprocess.Popen(["cat", "{}/temp".format(element)], stdout=subprocess.PIPE)
            data_from_command = self._process.communicate()[0].decode()
            self._process.stdout.close()
            thermal_data[counter] = int(int(data_from_command)/1000)
            counter += 1
        self.data = thermal_data


def main():
    c = CPUCoreTemperature()
    print(c.read())


if __name__ == "__main__":
    main()