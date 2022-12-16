from typing import List
import os
import posixpath
import tempfile
from abc import abstractmethod, ABCMeta
from collections import namedtuple


class ArtifactRepository:
    """
    Abstract artifact repo that defines how to upload and download potentially large
    artifacts from different storage backends.
    """

    __metaclass__ = ABCMeta

    def __init__(self, artifact_uri: str) -> None:
        self.artifact_uri = artifact_uri

    @abstractmethod
    def download_artifact(self, artifact_url: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def download_artifacts(self, artifact_urls: List[str]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def parse_url_to_destination(self, artifact_url: str) -> str:
        raise NotImplementedError()
