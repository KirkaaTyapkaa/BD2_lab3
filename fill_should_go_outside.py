from app.config import SessionLocal
from app.services.precipitation_service import fill_should_go_outside


def main():
    session = SessionLocal()
    try:
        fill_should_go_outside(session)
    finally:
        session.close()


if __name__ == "__main__":
    main()
