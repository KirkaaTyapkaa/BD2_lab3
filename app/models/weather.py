import enum

from sqlalchemy import Column, Integer, Float, String, DateTime, Time, Enum
from app.config import Base


class WindDirection(enum.Enum):
    N = "N"
    NNE = "NNE"
    NE = "NE"
    ENE = "ENE"
    E = "E"
    ESE = "ESE"
    SE = "SE"
    SSE = "SSE"
    S = "S"
    SSW = "SSW"
    SW = "SW"
    WSW = "WSW"
    W = "W"
    WNW = "WNW"
    NW = "NW"
    NNW = "NNW"


class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Обов'язкові колонки
    country = Column(String, nullable=False)                          # текстова
    wind_degree = Column(Integer)                                     # ціле число
    wind_kph = Column(Float)                                          # дробне число
    wind_direction = Column(Enum(WindDirection), nullable=True)       # enum
    last_updated = Column(DateTime, nullable=True)                    # дата
    sunrise = Column(Time, nullable=True)                             # час

    # Колонки категорії "Осади" (варіант 3)
    precip_mm = Column(Float)
    precip_in = Column(Float)
    humidity = Column(Integer)
    cloud = Column(Integer)
    visibility_km = Column(Float)
    visibility_miles = Column(Float)
