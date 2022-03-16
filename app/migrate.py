from alembic.command import upgrade
from alembic.config import Config


def run_sql_migrations(db, migrations_path: str) -> None:
    config = Config()
    config.set_main_option("script_location", migrations_path)
    config.set_main_option("sqlalchemy.url", str(db.engine.url))
    upgrade(config, "head")
