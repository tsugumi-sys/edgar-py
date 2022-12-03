from typing import Dict

import requests

from ...db.crud.submission_json import SubmissionJsonDB
from ..dataloader_interface import DataLoaderInterface


class SubmissionDataLoader(DataLoaderInterface):
    endpoint_url = "https://data.sec.gov/submissions/"
    headers = {"User-Agent": "exampleEmail@gmail.com"}

    def __init__(self, db_uri: str) -> None:
        self.sumission_db = SubmissionJsonDB(db_uri)
        super().__init__()
        
    def _check_exists(self, cik: str) -> bool:
         

    def get_submission_data_url(self, cik: str) -> str:
        return f"{self.endpoint_url}/CIK{cik}.json"

    def get_company_submissions(self, cik: str) -> Dict:
        return requests.get(
            self.get_submission_data_url(cik), headers=self.headers
        ).json()
    
    @property
    def _raw_folder(self) -> str:
        return 
