from typing import Dict, List, Union
import os
import time

from sqlalchemy import select, insert


from ...db import schemas, models
from ..database import BaseSession


class SubmissionJsonDB:
    def __init__(self, uri: str):
        self.session = BaseSession(uri).session

    def insert_items(self, items: List[Dict]) -> None:
        """
        Args:
            items (List[Dict]): {cik: str, save_path: str}
        """
        is_all_save_path_valid = all(os.path.isabs(i["save_path"]) for i in items)
        if not is_all_save_path_valid:
            raise ValueError("save_path should be absolute path. not relative path")

        for item in items:
            item["save_unixtimestamp"] = str(int(time.time()))

        with self.session.begin() as db:
            db.execute(insert(models.SubmissionJson.__table__), items)
            db.commit()

    def get_submission_json_info(
        self, ciks: Union[str, List[str]]
    ) -> List[schemas.SubmissionJson]:
        if not isinstance(ciks, str) or not isinstance(ciks, List):
            raise ValueError("tickers should be str or List[str]")

        if isinstance(ciks, str):
            ciks = [ciks]
        results = {}
        with self.session.begin() as db:
            results = db.execute(
                select(models.SubmissionJson.__table__)
                .where(models.SubmissionJson.cik._in(ciks))
                .all()
            )
        return [schemas.SubmissionJson(**item) for item in results]
