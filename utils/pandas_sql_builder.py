
def pandasSQL_builder(
    con,
    schema: str | None = None,
    need_transaction: bool = False,
) -> PandasSQL:
    """
    Convenience function to return the correct PandasSQL subclass based on the
    provided parameters.  Also creates a sqlalchemy connection and transaction
    if necessary.
    """
    import sqlite3

    if isinstance(con, sqlite3.Connection) or con is None:
        return SQLiteDatabase(con)

    sqlalchemy = import_optional_dependency("sqlalchemy", errors="ignore")

    if isinstance(con, str) and sqlalchemy is None:
        raise ImportError(
            f"Using URI string without version '{VERSIONS['sqlalchemy']}' or newer "
            "of 'sqlalchemy' installed."
        )

    if sqlalchemy is not None and isinstance(con, (str, sqlalchemy.engine.Connectable)):
        return SQLDatabase(con, schema, need_transaction)

    adbc = import_optional_dependency("adbc_driver_manager.dbapi", errors="ignore")
    if adbc and isinstance(con, adbc.Connection):
        return ADBCDatabase(con)

    warnings.warn(
        "pandas only supports SQLAlchemy connectable (engine/connection) or "
        "database string URI or sqlite3 DBAPI2 connection. Other DBAPI2 "
        "objects are not tested. Please consider using SQLAlchemy.",
        UserWarning,
        stacklevel=find_stack_level(),
    )
    return SQLiteDatabase(con)

