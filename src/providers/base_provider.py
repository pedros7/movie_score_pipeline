import abc

class BaseProvider(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fetch(self, url):
        pass
