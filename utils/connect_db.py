
def connect_db(db_file: str, set_journal_mode: bool) -> sqlite3.Connection:
    import sqlite3.dbapi2

    db = sqlite3.dbapi2.connect(db_file, check_same_thread=False)
    # This is a bit unfortunate (as we may get corrupt cache after e.g. Ctrl + C),
    # but without this flag, commits are *very* slow, especially when using HDDs,
    # see https://www.sqlite.org/faq.html#q19 for details.
    db.execute("PRAGMA synchronous=OFF")
    if set_journal_mode:
        db.execute("PRAGMA journal_mode=WAL")
    db.executescript(SCHEMA)
    return db

