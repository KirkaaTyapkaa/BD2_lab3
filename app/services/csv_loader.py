from datetime import datetime

import pandas as pd
from sqlalchemy.orm import Session

from app.models.weather import Weather, WindDirection


def _parse_time(val):
    """Парсить час у форматі '04:50 AM' -> datetime.time."""
    if pd.isna(val):
        return None
    try:
        return datetime.strptime(val.strip(), "%I:%M %p").time()
    except (ValueError, AttributeError):
        return None


def _parse_datetime(val):
    if pd.isna(val):
        return None
    try:
        return datetime.strptime(str(val).strip(), "%Y-%m-%d %H:%M")
    except (ValueError, AttributeError):
        return None


def _parse_wind_direction(val):
    if pd.isna(val):
        return None
    try:
        return WindDirection(val.strip())
    except (ValueError, KeyError):
        return None


def load_csv_to_db(csv_path: str, session: Session):
    """Зчитує CSV та завантажує дані в таблицю weather."""
    df = pd.read_csv(csv_path)

    records = []
    for _, row in df.iterrows():
        record = Weather(
            country=row["country"],
            wind_degree=int(row["wind_degree"]) if pd.notna(row["wind_degree"]) else None,
            wind_kph=float(row["wind_kph"]) if pd.notna(row["wind_kph"]) else None,
            wind_direction=_parse_wind_direction(row["wind_direction"]),
            last_updated=_parse_datetime(row["last_updated"]),
            sunrise=_parse_time(row["sunrise"]),
            precip_mm=float(row["precip_mm"]) if pd.notna(row["precip_mm"]) else None,
            precip_in=float(row["precip_in"]) if pd.notna(row["precip_in"]) else None,
            humidity=int(row["humidity"]) if pd.notna(row["humidity"]) else None,
            cloud=int(row["cloud"]) if pd.notna(row["cloud"]) else None,
            visibility_km=float(row["visibility_km"]) if pd.notna(row["visibility_km"]) else None,
            visibility_miles=float(row["visibility_miles"]) if pd.notna(row["visibility_miles"]) else None,
        )
        records.append(record)

    session.add_all(records)
    session.commit()
    print(f"Завантажено {len(records)} записів у базу даних.")
