from datetime import datetime

from app.config import SessionLocal
from app.repositories.weather_repository import WeatherRepository
from app.models.weather import Weather, Precipitation


def format_weather(w: Weather):
    """Форматує один запис погоди для виводу в консоль."""
    p: Precipitation = w.precipitation

    print(f"  Країна: {w.country}")
    print(f"  Дата оновлення: {w.last_updated}")
    print(f"  Схід сонця: {w.sunrise}")
    print(f"  Вітер: {w.wind_kph} км/год, напрямок {w.wind_direction.value if w.wind_direction else '—'}, {w.wind_degree}°")

    if p:
        print(f"  Опади: {p.precip_mm} мм ({p.precip_in} in)")
        print(f"  Вологість: {p.humidity}%")
        print(f"  Хмарність: {p.cloud}%")
        print(f"  Видимість: {p.visibility_km} км ({p.visibility_miles} миль)")
        if p.should_go_outside is not None:
            answer = "Так" if p.should_go_outside else "Ні"
            print(f"  Чи варто виходити на вулицю? {answer}")
    print()


def run():
    session = SessionLocal()
    repo = WeatherRepository(session)

    try:
        while True:
            print("=" * 50)
            print("Пошук погоди по країні та даті")
            print("(введіть 'вихід' для завершення)")
            print("=" * 50)

            country = input("Країна (англійською, напр. Ukraine): ").strip()
            if country.lower() in ("вихід", "exit", "q"):
                break

            date_str = input("Дата (YYYY-MM-DD, напр. 2024-05-16): ").strip()
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                print("Невірний формат дати. Спробуйте ще раз.\n")
                continue

            results = repo.get_by_country_and_date(country, date)

            if not results:
                print(f"\nДаних для {country} за {date} не знайдено.\n")
                continue

            print(f"\nЗнайдено {len(results)} запис(ів) для {country} за {date}:\n")
            for i, w in enumerate(results, 1):
                print(f"--- Запис {i} ---")
                format_weather(w)

    finally:
        session.close()
