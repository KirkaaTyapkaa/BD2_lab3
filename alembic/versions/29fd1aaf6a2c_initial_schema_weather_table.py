"""initial schema - weather table

Revision ID: 29fd1aaf6a2c
Revises:
Create Date: 2026-04-19 18:09:19.209694

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29fd1aaf6a2c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('weather',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('country', sa.String(length=255), nullable=False),
        sa.Column('wind_degree', sa.Integer(), nullable=True),
        sa.Column('wind_kph', sa.Float(), nullable=True),
        sa.Column('wind_direction', sa.Enum(
            'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
            'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW',
            name='winddirection'
        ), nullable=True),
        sa.Column('last_updated', sa.DateTime(), nullable=True),
        sa.Column('sunrise', sa.Time(), nullable=True),
        sa.Column('precip_mm', sa.Float(), nullable=True),
        sa.Column('precip_in', sa.Float(), nullable=True),
        sa.Column('humidity', sa.Integer(), nullable=True),
        sa.Column('cloud', sa.Integer(), nullable=True),
        sa.Column('visibility_km', sa.Float(), nullable=True),
        sa.Column('visibility_miles', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('weather')
    # Видаляємо тип Enum (в PostgreSQL це окремий об'єкт, в MySQL — ні)
    sa.Enum(name='winddirection').drop(op.get_bind(), checkfirst=True)
