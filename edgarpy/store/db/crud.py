from typing import Dict, Union, List
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.engine.row import Row
from sqlalchemy.exc import NoResultFound

from ..db import schemas, models
from .database import BaseSession


class CompanyDB:
    def __init__(self, uri: str):
        self.session = BaseSession(uri).session

    def insert_company_items(self, items: List) -> None:
        """
        Args:
            items (Dict): {id: str, cik: str, ticker: str, title: str}
        """
        with self.session.begin() as db:
            db.execute(models.Company.__table__.insert(), items)
            db.commit()

    def get_cik_by_tickers(self, tickers: Union[str, List[str]]) -> Union[str, Dict]:
        if isinstance(tickers, str):
            with self.session.begin() as db:
                cik = (
                    db.query(models.Company)
                    .filter(models.Company.ticker == tickers)
                    .one()
                    .cik
                )

            return cik
        elif isinstance(tickers, List):
            results = {}
            with self.session.begin() as db:
                for ticker in tickers:
                    try:
                        cik = (
                            db.query(models.Company)
                            .filter(models.Company.ticker == ticker)
                            .one()
                            .cik
                        )
                    except NoResultFound:
                        cik = None
                    results[ticker] = cik
            return results
        else:
            raise ValueError("tickers should be str or List[str]")
