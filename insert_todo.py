import sys
import app
from app import database as db


if len(sys.argv) < 2:
    print("Missing todo text", file=sys.stderr)
    sys.exit(1)

engine = app.init_connection_engine()
if engine is not None:
    task_id = db.insert_new_task(sys.argv[1])
else:
    print("There is no DB configured", file=sys.stderr)
