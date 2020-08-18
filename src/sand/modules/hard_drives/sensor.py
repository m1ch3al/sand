import subprocess

from sand.sensor_module import HardwareSensorModule


class HardDriveSensor(HardwareSensorModule):
    def __init__(self, list_of_partitions):
        HardwareSensorModule.__init__(self)
        self._process = None
        self._list_of_partitions = list_of_partitions
        self.data = dict()
        for partition in self._list_of_partitions:
            self.data[partition] = None

    def run_command(self):
        for single_partition in self._list_of_partitions:
            self._process = subprocess.Popen(["df", "-TH", "{}".format(single_partition)], stdout=subprocess.PIPE)
            data_from_command = self._process.communicate()[0].decode()
            self._process.stdout.close()
            self.data[single_partition] = self._build_single_partition_information(data_from_command)

    def _build_single_partition_information(self, process_data):
        splitted = process_data.split("\n")
        splitted_information = splitted[1].split(" ")
        partition_information = dict()
        mapper = ["filesystem", "type", "size", "used", "free", "used_percentage", "mount_pount"]

        for element in mapper:
            for component in splitted_information:
                if len(component) > 0:
                    partition_information[mapper[0]] = component
                    mapper.pop(0)
        return partition_information
