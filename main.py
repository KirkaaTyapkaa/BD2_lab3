"""
Розгортання бази даних з нуля:
1. Alembic-міграції створюють структуру (всі таблиці)
2. CSV loader заповнює дані
3. Сервіс заповнює колонку should_go_outside
"""
from alembic.config import Config
from alembic import command

from app.config import SessionLocal
from app.services.csv_loader import load_csv_to_db
from app.services.precipitation_service import fill_should_go_outside


def main():
    # 1. Накочуємо всі міграції
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    print("Міграції накочені.")

    # 2. Завантажуємо дані з CSV
    session = SessionLocal()
    try:
        load_csv_to_db("GlobalWeatherRepository.csv", session)

        # 3. Заповнюємо should_go_outside
        fill_should_go_outside(session)
    finally:
        session.close()


if __name__ == "__main__":
    main()
