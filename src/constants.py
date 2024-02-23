SQLITE_DB_FILE_PATH = "emails.db"
SQLITE_DB_INIT_STATEMENT = "CREATE TABLE target (uid, email, timestamp)"
SQLITE_DB_CREATE_RECORD_STATEMENT = "INSERT INTO target VALUES (?, ?, ?)"
SQLITE_DB_GET_RECORD_STATEMENT = "SELECT * FROM target WHERE uid = ? LIMIT 1"
SQLITE_DB_UPDATE_RECORD_STATEMENT = "UPDATE target SET timestamp = ? WHERE uid = ?"

EMAIL_SUBJECT = "Дыня не дамажит"
EMAIL_BODY = """
АЗАЗАЗЗАЗАЗАЗЗАЗАЗА
<img src="%s" alt="img" />
"""
