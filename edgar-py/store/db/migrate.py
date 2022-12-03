from .database import BaseEngine
from .models import Base


class Migration:
    def __init__(self, uri: str):
        self.engine = BaseEngine(uri).engine

    def run(self):
        Base.metadata.create_all(self.engine)
