from pydantic import BaseModel


class Company(BaseModel):
    id: str
    cik: str
    ticker: str
    title: str


class SubmissionJson(BaseModel):
    cik: str
    save_unixtimestamp: str
    save_path: str
