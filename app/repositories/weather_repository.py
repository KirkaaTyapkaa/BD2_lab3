from sqlalchemy.orm import Session
from app.models.weather import Weather


class WeatherRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_all(self, records: list[Weather]):
        self.session.add_all(records)
        self.session.commit()

    def get_by_country_and_date(self, country: str, date) -> list[Weather]:
        from sqlalchemy import func
        return (
            self.session.query(Weather)
            .filter(
                func.lower(Weather.country) == country.lower(),
                func.date(Weather.last_updated) == date,
            )
            .all()
        )
