from typing import Dict, Union, List
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from sqlalchemy.engine.row import Row
from sqlalchemy.exc import NoResultFound

from ...db import schemas, models
from ..database import BaseSession


class CompanyDB:
    def __init__(self, uri: str):
        self.session = BaseSession(uri).session

    def insert_items(self, items: List[Dict]) -> None:
        """
        Args:
            items (List[Dict]): {id: str, cik: str, ticker: str, title: str}
        """
        with self.session.begin() as db:
            db.execute(insert(models.Company.__table__), items)
            db.commit()

    def get_cik_by_tickers(self, tickers: Union[str, List[str]]) -> Union[str, Dict]:
        if not isinstance(tickers, str) or not isinstance(tickers, List):
            raise ValueError("tickers should be str or List[str]")

        if isinstance(tickers, str):
            tickers = [tickers]
        results = {}
        with self.session.begin() as db:
            for ticker in tickers:
                try:
                    cik = (
                        select(models.Company.__table__)
                        .where(models.Company.ticker == ticker)
                        .one()
                        .cik
                    )
                except NoResultFound:
                    cik = None
                results[ticker] = cik
        return results
