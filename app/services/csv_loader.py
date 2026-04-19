from datetime import datetime

import pandas as pd
from sqlalchemy.orm import Session

from app.models.weather import Weather, Precipitation, WindDirection

BATCH_SIZE = 10000


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
    """Зчитує CSV та завантажує дані в таблиці weather та precipitation."""
    df = pd.read_csv(csv_path)

    weather_batch = []
    precip_batch = []

    for i, (_, row) in enumerate(df.iterrows(), 1):
        weather = Weather(
            country=row["country"],
            wind_degree=int(row["wind_degree"]) if pd.notna(row["wind_degree"]) else None,
            wind_kph=float(row["wind_kph"]) if pd.notna(row["wind_kph"]) else None,
            wind_direction=_parse_wind_direction(row["wind_direction"]),
            last_updated=_parse_datetime(row["last_updated"]),
            sunrise=_parse_time(row["sunrise"]),
        )
        session.add(weather)
        weather_batch.append(weather)

        precip_batch.append({
            "precip_mm": float(row["precip_mm"]) if pd.notna(row["precip_mm"]) else None,
            "precip_in": float(row["precip_in"]) if pd.notna(row["precip_in"]) else None,
            "humidity": int(row["humidity"]) if pd.notna(row["humidity"]) else None,
            "cloud": int(row["cloud"]) if pd.notna(row["cloud"]) else None,
            "visibility_km": float(row["visibility_km"]) if pd.notna(row["visibility_km"]) else None,
            "visibility_miles": float(row["visibility_miles"]) if pd.notna(row["visibility_miles"]) else None,
        })

        if i % BATCH_SIZE == 0:
            session.flush()
            for w, p_data in zip(weather_batch, precip_batch):
                session.add(Precipitation(weather_id=w.id, **p_data))
            session.commit()
            weather_batch = []
            precip_batch = []
            print(f"  {i} записів...")

    # Залишок
    if weather_batch:
        session.flush()
        for w, p_data in zip(weather_batch, precip_batch):
            session.add(Precipitation(weather_id=w.id, **p_data))
        session.commit()

    print(f"Завантажено {len(df)} записів у базу даних.")
