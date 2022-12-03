from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Company(Base):
    __tablename__ = "company"
    id = Column(String, primary_key=True, unique=True)
    cik = Column(String, unique=False)
    ticker = Column(String, unique=False)
    title = Column(String, unique=False)


class SubmissionJson(Base):
    __tablename__ = "submission_json"
    cik = Column(String)
    save_unixtimestamp = Column(String)
    save_path = Column(String, unique=True)
