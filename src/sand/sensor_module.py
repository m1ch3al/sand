from abc import ABC, abstractmethod


class HardwareSensorModule(ABC):
    def __init__(self):
        super().__init__()
        self.data = None

    @abstractmethod
    def run_command(self):
        pass

    def read(self):
        self.run_command()
        return self.data
