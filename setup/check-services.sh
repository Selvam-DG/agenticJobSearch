
#!/usr/bin/env bash

set -euo pipefail

: "${DATABASE_URL:?Set DATABASE_URL first}"

echo "Testing PostgreSQL connection..."

python -c '
from sqlalchemy import create_engine, text
import os

engine = create_engine(os.environ["DATABASE_URL"])

with engine.connect() as connection:
    version = connection.execute(
        text("SELECT version()")
    ).scalar()

    print(version.split(",")[0])

engine.dispose()
'

echo "PostgreSQL is reachable."
