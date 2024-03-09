import uuid
import logging
import sqlite3
from typing import Any
from functools import cache
from datetime import datetime, timezone

from .constants import *

parse_uuid = uuid.UUID

logging.basicConfig(level=logging.DEBUG)
sqlite3.register_adapter(parse_uuid, lambda u: u.bytes_le)
sqlite3.register_converter("GUID", lambda b: parse_uuid(bytes_le=b))


@cache
def create_image(width: int = 5, height: int = 5, channels: int = 4) -> bytes:
    import io
    import numpy as np
    from PIL import Image

    np_img = np.zeros((width, height, channels), dtype=np.uint8)
    pil_img = Image.fromarray(np_img)

    with io.BytesIO() as buf:
        pil_img.save(buf, format="png")
        pil_bytes = buf.getvalue()
    return pil_bytes


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


def create_record(email: str) -> tuple[Any]:
    args = uuid.uuid4(), uuid.uuid3(uuid.NAMESPACE_DNS, email), email, None

    conn = sqlite3.connect(SQLITE_DB_FILE_PATH)
    conn.cursor().execute(SQLITE_DB_CREATE_RECORD_STATEMENT, args)
    conn.commit()

    logging.debug(f"Created record {args}")
    conn.close()

    return args


def get_record(uid: str) -> tuple[Any]:
    args = parse_uuid(uid),
    if args[0].version() == 4:
        statement = SQLITE_DB_GET_U_RECORD_STATEMENT
    else:
        statement = SQLITE_DB_GET_I_RECORD_STATEMENT

    conn = sqlite3.connect(SQLITE_DB_FILE_PATH)
    res = conn.cursor().execute(statement, args).fetchone()
    logging.debug(f"Got record {res}")
    conn.close()

    return res


def update_record(uid: str) -> None:
    args = datetime.now(timezone.utc), parse_uuid(uid)
    if args[1].version() != 4:
        return

    conn = sqlite3.connect(SQLITE_DB_FILE_PATH)
    conn.cursor().execute(SQLITE_DB_UPDATE_RECORD_STATEMENT, args)
    conn.commit()

    logging.debug(f"Updated record {args}")
    conn.close()
