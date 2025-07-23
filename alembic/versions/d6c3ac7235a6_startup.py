"""startup

Revision ID: d6c3ac7235a6
Revises:
Create Date: 2025-07-23 12:55:44.899279

"""

from typing import Sequence, Union

from alembic import op
import os


# revision identifiers, used by Alembic.
revision: str = "d6c3ac7235a6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SQL_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "scripts", "install_uuid-ossp.sql"
)


def upgrade() -> None:
    with open(SQL_FILE_PATH, "r") as script:
        sql_script = script.read()

    op.execute(sql_script)


def downgrade() -> None:
    pass
