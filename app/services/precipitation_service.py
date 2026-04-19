from sqlalchemy.orm import Session
from app.models.weather import Precipitation


def calculate_should_go_outside(p: Precipitation) -> bool:
    """
    Формула: варто виходити на вулицю якщо:
    - опади менше 5 мм
    - вологість менше 85%
    - видимість більше 2 км
    """
    precip_ok = (p.precip_mm or 0) < 5
    humidity_ok = (p.humidity or 0) < 85
    visibility_ok = (p.visibility_km or 0) > 2
    return precip_ok and humidity_ok and visibility_ok


def fill_should_go_outside(session: Session):
    """Заповнює колонку should_go_outside для всіх записів."""
    records = session.query(Precipitation).all()
    for record in records:
        record.should_go_outside = calculate_should_go_outside(record)
    session.commit()
    print(f"Оновлено {len(records)} записів у колонці should_go_outside.")
