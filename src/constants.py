SQLITE_DB_FILE_PATH = "emails.sqlite"
SQLITE_DB_INIT_STATEMENT = """
CREATE TABLE target (
    uid GUID PRIMARY KEY,
    iid GUID NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    timestamp DATETIME
)
""".strip()
SQLITE_DB_CREATE_RECORD_STATEMENT = "INSERT INTO target VALUES (?, ?, ?, ?)"
SQLITE_DB_GET_U_RECORD_STATEMENT = "SELECT * FROM target WHERE uid = ? LIMIT 1"
SQLITE_DB_GET_I_RECORD_STATEMENT = "SELECT * FROM target WHERE iid = ? LIMIT 1"
SQLITE_DB_UPDATE_RECORD_STATEMENT = "UPDATE target SET timestamp = ? WHERE uid = ?"

EMAIL_SUBJECT = "Дыня не дамажит"
EMAIL_BODY = """
ПРОИЗОШЕЛ ВЗЛОМ ЖЕПЫ
<br>
<img src="%s" alt="img" />
<img src="%s" alt="img" />
"""
