from app.config import engine, SessionLocal, Base
from app.services.csv_loader import load_csv_to_db


def main():
    # Створюємо таблиці
    Base.metadata.create_all(engine)
    print("Таблиці створено.")

    # Завантажуємо дані з CSV
    session = SessionLocal()
    try:
        load_csv_to_db("GlobalWeatherRepository.csv", session)
    finally:
        session.close()


if __name__ == "__main__":
    main()
