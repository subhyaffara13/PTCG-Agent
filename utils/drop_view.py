
def drop_view(
    view_name: str,
    conn: sqlite3.Connection | sqlalchemy.engine.Engine | sqlalchemy.engine.Connection,
):
    import sqlalchemy

    if isinstance(conn, sqlite3.Connection):
        conn.execute(f"DROP VIEW IF EXISTS {sql._get_valid_sqlite_name(view_name)}")
        conn.commit()
    else:
        adbc = import_optional_dependency("adbc_driver_manager.dbapi", errors="ignore")
        if adbc and isinstance(conn, adbc.Connection):
            with conn.cursor() as cur:
                cur.execute(f'DROP VIEW IF EXISTS "{view_name}"')
        else:
            quoted_view = conn.engine.dialect.identifier_preparer.quote_identifier(
                view_name
            )
            stmt = sqlalchemy.text(f"DROP VIEW IF EXISTS {quoted_view}")
            with conn.begin() as con:
                con.execute(stmt)  # type: ignore[union-attr]

