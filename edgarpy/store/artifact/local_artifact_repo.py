from typing import List
import os
import shutil
from urllib.parse import urlparse

from edgarpy.store.artifact.artifact_repo import ArtifactRepository


class LocalArtifactRepository(ArtifactRepository):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._artifact_dir = local_file_uri_to_path(self.artifact_uri)
        
    @property
    def artifact_dir(self):
        return self._artifact_dir
    
    def download_artifact(self, artifact_url: str) -> None:
        return super().download_artifact(artifact_url)
    
    def download_artifacts(self, artifact_urls: List[str]) -> None:
        return super().download_artifacts(artifact_urls)
    
    def parse_url_to_destination(self, artifact_url: str) -> str:
        parsed_url = urlparse(artifact_url)
        if parsed_url.scheme == '' or parsed_url.netloc == '' or parsed_url.path == '':
            raise ValueError(f'Invalid artifact_url: {artifact_url}')
        
        return os.path.join(self.artifact_dir, parsed_url.path)
