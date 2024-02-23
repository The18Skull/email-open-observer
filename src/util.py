import logging
import sqlite3
from uuid import uuid4
from typing import Any
from functools import cache
from datetime import datetime, timezone

from .constants import *

logging.basicConfig(level=logging.DEBUG)


@cache
def create_image(width: int = 5, height: int = 5, channels: int = 4) -> bytes:
    import numpy as np
    return np.zeros((width, height, channels), dtype=np.uint8).tobytes()


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
    args = str(uuid4()), email, None

    conn = sqlite3.connect(SQLITE_DB_FILE_PATH)
    conn.execute(SQLITE_DB_CREATE_RECORD_STATEMENT, args)
    logging.debug(f"Created record {args}")
    conn.close()

    return args[0]


def get_record(uid: str) -> tuple[Any]:
    args = uid,

    conn = sqlite3.connect(SQLITE_DB_FILE_PATH)
    res = conn.execute(SQLITE_DB_GET_RECORD_STATEMENT, args).fetchone()
    logging.debug(f"Got record {res}")
    conn.close()

    return res


def update_record(uid: str) -> None:
    args = uid, datetime.now(timezone.utc)

    conn = sqlite3.connect(SQLITE_DB_FILE_PATH)
    conn.execute(SQLITE_DB_UPDATE_RECORD_STATEMENT, args)
    logging.debug(f"Updated record {args}")
    conn.close()
