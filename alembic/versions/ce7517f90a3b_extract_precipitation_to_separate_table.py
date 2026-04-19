"""extract precipitation to separate table

Revision ID: ce7517f90a3b
Revises: 29fd1aaf6a2c
Create Date: 2026-04-19 18:35:33.662513

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce7517f90a3b'
down_revision: Union[str, Sequence[str], None] = '29fd1aaf6a2c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Створюємо нову таблицю precipitation
    op.create_table('precipitation',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('weather_id', sa.Integer(), nullable=False),
        sa.Column('precip_mm', sa.Float(), nullable=True),
        sa.Column('precip_in', sa.Float(), nullable=True),
        sa.Column('humidity', sa.Integer(), nullable=True),
        sa.Column('cloud', sa.Integer(), nullable=True),
        sa.Column('visibility_km', sa.Float(), nullable=True),
        sa.Column('visibility_miles', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['weather_id'], ['weather.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('weather_id')
    )

    # 2. Переносимо дані з weather в precipitation
    op.execute(sa.text(
        "INSERT INTO precipitation (weather_id, precip_mm, precip_in, humidity, cloud, visibility_km, visibility_miles) "
        "SELECT id, precip_mm, precip_in, humidity, cloud, visibility_km, visibility_miles FROM weather"
    ))

    # 3. Видаляємо колонки осадів з weather
    op.drop_column('weather', 'cloud')
    op.drop_column('weather', 'visibility_km')
    op.drop_column('weather', 'humidity')
    op.drop_column('weather', 'precip_mm')
    op.drop_column('weather', 'visibility_miles')
    op.drop_column('weather', 'precip_in')


def downgrade() -> None:
    """Downgrade schema."""
    # 1. Повертаємо колонки в weather
    op.add_column('weather', sa.Column('precip_in', sa.Float(), nullable=True))
    op.add_column('weather', sa.Column('visibility_miles', sa.Float(), nullable=True))
    op.add_column('weather', sa.Column('precip_mm', sa.Float(), nullable=True))
    op.add_column('weather', sa.Column('humidity', sa.Integer(), nullable=True))
    op.add_column('weather', sa.Column('visibility_km', sa.Float(), nullable=True))
    op.add_column('weather', sa.Column('cloud', sa.Integer(), nullable=True))

    # 2. Переносимо дані назад (універсальний SQL через підзапити)
    op.execute(sa.text(
        "UPDATE weather SET "
        "precip_mm = (SELECT p.precip_mm FROM precipitation p WHERE p.weather_id = weather.id), "
        "precip_in = (SELECT p.precip_in FROM precipitation p WHERE p.weather_id = weather.id), "
        "humidity = (SELECT p.humidity FROM precipitation p WHERE p.weather_id = weather.id), "
        "cloud = (SELECT p.cloud FROM precipitation p WHERE p.weather_id = weather.id), "
        "visibility_km = (SELECT p.visibility_km FROM precipitation p WHERE p.weather_id = weather.id), "
        "visibility_miles = (SELECT p.visibility_miles FROM precipitation p WHERE p.weather_id = weather.id) "
        "WHERE EXISTS (SELECT 1 FROM precipitation p WHERE p.weather_id = weather.id)"
    ))

    # 3. Видаляємо таблицю precipitation
    op.drop_table('precipitation')
