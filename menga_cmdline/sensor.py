from abc import ABCMeta, abstractmethod

class Sensor(metaclass=ABCMeta):
    
    @staticmethod
    @abstractmethod
    def start():
        """Abstract method to run sensor"""

    @staticmethod
    @abstractmethod
    def stop():
        """Abstract method to run sensor"""

    @staticmethod
    @abstractmethod
    def get_files():
        """Abstract method to run sensor"""   
    
    @staticmethod
    @abstractmethod
    def get_file():
        """Abstract method to run sensor""" 