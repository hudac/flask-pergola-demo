"""init db

Revision ID: cfd322bfde16
Revises: 
Create Date: 2022-03-15 18:50:48.004049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfd322bfde16'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE TABLE tasks (
            id serial NOT NULL,
            task varchar NOT NULL,
            status varchar,
        PRIMARY KEY (id)
    );
    """)
    op.execute("INSERT INTO tasks (task, status) VALUES ('task no.1' , 'Todo');")
    op.execute("INSERT INTO tasks (task, status) VALUES ('task no.2' , 'Todo');")
    op.execute("INSERT INTO tasks (task, status) VALUES ('task no.3' , 'Todo');")


def downgrade():
    op.drop_table(table_name="tasks")
