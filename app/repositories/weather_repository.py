from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from app.models.weather import Weather


class WeatherRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_all(self, records: list[Weather]):
        self.session.add_all(records)
        self.session.commit()

    def get_by_country_and_date(self, country: str, date) -> list[Weather]:
        return (
            self.session.query(Weather)
            .options(joinedload(Weather.precipitation))
            .filter(
                func.lower(Weather.country) == country.lower(),
                func.date(Weather.last_updated) == date,
            )
            .all()
        )

    def get_available_countries(self) -> list[str]:
        return [
            row[0] for row in
            self.session.query(Weather.country).distinct().order_by(Weather.country).all()
        ]
