
def get_schema(
    frame,
    name: str,
    keys=None,
    con=None,
    dtype: DtypeArg | None = None,
    schema: str | None = None,
) -> str:
    """
    Get the SQL db table schema for the given frame.

    Parameters
    ----------
    frame : DataFrame
    name : str
        name of SQL table
    keys : string or sequence, default: None
        columns to use a primary key
    con: ADBC Connection, SQLAlchemy connectable, sqlite3 connection, default: None
        ADBC provides high performance I/O with native type support, where available.
        Using SQLAlchemy makes it possible to use any DB supported by that
        library
        If a DBAPI2 object, only sqlite3 is supported.
    dtype : dict of column name to SQL type, default None
        Optional specifying the datatype for columns. The SQL type should
        be a SQLAlchemy type, or a string for sqlite3 fallback connection.
    schema: str, default: None
        Optional specifying the schema to be used in creating the table.
    """
    with pandasSQL_builder(con=con) as pandas_sql:
        return pandas_sql._create_sql_schema(
            frame, name, keys=keys, dtype=dtype, schema=schema
        )

