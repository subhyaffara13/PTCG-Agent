
def drop_table(
    table_name: str,
    conn: sqlite3.Connection | sqlalchemy.engine.Engine | sqlalchemy.engine.Connection,
):
    if isinstance(conn, sqlite3.Connection):
        conn.execute(f"DROP TABLE IF EXISTS {sql._get_valid_sqlite_name(table_name)}")
        conn.commit()

    else:
        adbc = import_optional_dependency("adbc_driver_manager.dbapi", errors="ignore")
        if adbc and isinstance(conn, adbc.Connection):
            with conn.cursor() as cur:
                cur.execute(f'DROP TABLE IF EXISTS "{table_name}"')
        else:
            with conn.begin() as con:
                with sql.SQLDatabase(con) as db:
                    db.drop_table(table_name)

