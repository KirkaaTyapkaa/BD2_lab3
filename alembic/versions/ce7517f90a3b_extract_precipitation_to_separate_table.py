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
    op.execute("""
        INSERT INTO precipitation (weather_id, precip_mm, precip_in, humidity, cloud, visibility_km, visibility_miles)
        SELECT id, precip_mm, precip_in, humidity, cloud, visibility_km, visibility_miles
        FROM weather
    """)

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
    op.add_column('weather', sa.Column('precip_in', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('weather', sa.Column('visibility_miles', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('weather', sa.Column('precip_mm', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('weather', sa.Column('humidity', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('weather', sa.Column('visibility_km', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('weather', sa.Column('cloud', sa.INTEGER(), autoincrement=False, nullable=True))

    # 2. Переносимо дані назад
    op.execute("""
        UPDATE weather
        SET precip_mm = p.precip_mm,
            precip_in = p.precip_in,
            humidity = p.humidity,
            cloud = p.cloud,
            visibility_km = p.visibility_km,
            visibility_miles = p.visibility_miles
        FROM precipitation p
        WHERE weather.id = p.weather_id
    """)

    # 3. Видаляємо таблицю precipitation
    op.drop_table('precipitation')
