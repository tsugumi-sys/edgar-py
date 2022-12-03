from typing import Tuple

import sqlalchemy


class BaseEngine:
    # uri = "sqlite:///secdata.db"

    def __init__(self, uri: str):
        self.engine = sqlalchemy.create_engine(uri)


class BaseSession:
    def __init__(self, uri: str):
        engine = BaseEngine(uri).engine
        self.session = sqlalchemy.orm.sessionmaker(bind=engine)  # type: ignore
