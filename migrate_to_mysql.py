"""
Скрипт міграції з PostgreSQL на MySQL.
1. Накочує Alembic-міграції на MySQL (створює структуру)
2. Переносить всі дані з PostgreSQL в MySQL
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.config import POSTGRES_URL, MYSQL_URL
from app.models.weather import Weather, Precipitation  # noqa: F401

from alembic.config import Config
from alembic import command


def run_alembic_on_mysql():
    """Накочує всі Alembic-міграції на MySQL."""
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", MYSQL_URL)
    command.upgrade(alembic_cfg, "head")
    print("Alembic-міграції накочені на MySQL.")


def transfer_data():
    """Переносить дані з PostgreSQL в MySQL."""
    pg_engine = create_engine(POSTGRES_URL)
    my_engine = create_engine(MYSQL_URL)

    PgSession = sessionmaker(bind=pg_engine)
    MySession = sessionmaker(bind=my_engine)

    pg_session = PgSession()
    my_session = MySession()

    try:
        # Переносимо weather
        weather_records = pg_session.query(Weather).all()
        print(f"Зчитано {len(weather_records)} записів weather з PostgreSQL...")

        batch = []
        for i, w in enumerate(weather_records, 1):
            batch.append(Weather(
                id=w.id,
                country=w.country,
                wind_degree=w.wind_degree,
                wind_kph=w.wind_kph,
                wind_direction=w.wind_direction,
                last_updated=w.last_updated,
                sunrise=w.sunrise,
            ))
            if i % 10000 == 0:
                my_session.bulk_save_objects(batch)
                my_session.commit()
                batch = []
                print(f"  weather: {i} записів...")

        if batch:
            my_session.bulk_save_objects(batch)
            my_session.commit()

        print(f"Записано {len(weather_records)} записів weather в MySQL.")

        # Переносимо precipitation
        precip_records = pg_session.query(Precipitation).all()
        print(f"Зчитано {len(precip_records)} записів precipitation з PostgreSQL...")

        batch = []
        for i, p in enumerate(precip_records, 1):
            batch.append(Precipitation(
                id=p.id,
                weather_id=p.weather_id,
                precip_mm=p.precip_mm,
                precip_in=p.precip_in,
                humidity=p.humidity,
                cloud=p.cloud,
                visibility_km=p.visibility_km,
                visibility_miles=p.visibility_miles,
                should_go_outside=p.should_go_outside,
            ))
            if i % 10000 == 0:
                my_session.bulk_save_objects(batch)
                my_session.commit()
                batch = []
                print(f"  precipitation: {i} записів...")

        if batch:
            my_session.bulk_save_objects(batch)
            my_session.commit()

        print(f"Записано {len(precip_records)} записів precipitation в MySQL.")

    finally:
        pg_session.close()
        my_session.close()


def verify():
    """Перевіряє кількість записів в обох базах."""
    pg_engine = create_engine(POSTGRES_URL)
    my_engine = create_engine(MYSQL_URL)

    with pg_engine.connect() as conn:
        pg_w = conn.execute(text("SELECT count(*) FROM weather")).scalar()
        pg_p = conn.execute(text("SELECT count(*) FROM precipitation")).scalar()

    with my_engine.connect() as conn:
        my_w = conn.execute(text("SELECT count(*) FROM weather")).scalar()
        my_p = conn.execute(text("SELECT count(*) FROM precipitation")).scalar()

    print(f"\nPostgreSQL: weather={pg_w}, precipitation={pg_p}")
    print(f"MySQL:      weather={my_w}, precipitation={my_p}")
    print(f"Дані {'збігаються!' if pg_w == my_w and pg_p == my_p else 'НЕ збігаються!'}")


if __name__ == "__main__":
    print("=== Міграція з PostgreSQL на MySQL ===\n")
    run_alembic_on_mysql()
    transfer_data()
    verify()
