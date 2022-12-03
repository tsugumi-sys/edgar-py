from typing import Any
from abc import ABCMeta, abstractmethod


class DataLoaderInterface(metaclass=ABCMeta):
    @abstractmethod
    def _load_data(self, url: str) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def _check_exists(self, url: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def _download(self, url: str) -> None:
        raise NotImplementedError()

    @property
    @abstractmethod
    def _raw_folder(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def _raw_filename(self) -> str:
        raise NotImplementedError()
