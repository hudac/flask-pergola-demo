from alembic.command import upgrade
from alembic.config import Config


def run_sql_migrations(db, migrations_path: str) -> None:
    config = Config()
    config.set_main_option("script_location", migrations_path)
    config.set_main_option("sqlalchemy.url", db.engine.url.render_as_string(hide_password=False).replace("%", "%%"))
    upgrade(config, "head")
