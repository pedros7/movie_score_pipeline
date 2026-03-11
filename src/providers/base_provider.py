import abc
import pandas as pd

class BaseProvider(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fetch(self, url: str):
        pass

    @abc.abstractmethod
    def transform(self, data: pd.DataFrame):
        pass