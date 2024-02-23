import uuid
import logging
import sqlite3
from typing import Any
from functools import cache
from datetime import datetime, timezone

from .constants import *

logging.basicConfig(level=logging.DEBUG)
sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)
sqlite3.register_converter("GUID", lambda b: uuid.UUID(bytes_le=b))


@cache
def create_image(width: int = 5, height: int = 5, channels: int = 4) -> bytes:
    import numpy as np
    return np.full((width, height, channels), 255, dtype=np.uint8).tobytes()


@cache
def read_config(path: str = "config.yml") -> dict[str, Any]:
    from yaml import unsafe_load
    with open(path, "r") as f:
        return unsafe_load(f)


def create_db() -> None:
    import os
    if os.path.exists(SQLITE_DB_FILE_PATH):
        return

    import sqlite3
    conn = sqlite3.connect(SQLITE_DB_FILE_PATH)
    conn.execute(SQLITE_DB_INIT_STATEMENT)
    logging.info("Database was created")
    conn.close()


def create_record(email: str) -> str:
    args = uuid.uuid4(), email, None

    conn = sqlite3.connect(SQLITE_DB_FILE_PATH)
    conn.cursor().execute(SQLITE_DB_CREATE_RECORD_STATEMENT, args)
    conn.commit()

    logging.debug(f"Created record {args}")
    conn.close()

    return args[0]


def get_record(uid: str) -> tuple[Any]:
    args = uuid.UUID(uid),

    conn = sqlite3.connect(SQLITE_DB_FILE_PATH)
    res = conn.cursor().execute(SQLITE_DB_GET_RECORD_STATEMENT, args).fetchone()
    logging.debug(f"Got record {res}")
    conn.close()

    return res


def update_record(uid: str) -> None:
    args = datetime.now(timezone.utc), uuid.UUID(uid)

    conn = sqlite3.connect(SQLITE_DB_FILE_PATH)
    conn.cursor().execute(SQLITE_DB_UPDATE_RECORD_STATEMENT, args)
    conn.commit()

    logging.debug(f"Updated record {args}")
    conn.close()
