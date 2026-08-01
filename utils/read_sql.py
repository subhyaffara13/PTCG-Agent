
def read_sql(  # pyright: ignore[reportOverlappingOverload]
    sql,
    con,
    index_col: str | list[str] | None = ...,
    coerce_float=...,
    params=...,
    parse_dates=...,
    columns: list[str] = ...,
    chunksize: None = ...,
    dtype_backend: DtypeBackend | lib.NoDefault = ...,
    dtype: DtypeArg | None = None,
) -> DataFrame: ...


def read_sql(
    sql,
    con,
    index_col: str | list[str] | None = ...,
    coerce_float=...,
    params=...,
    parse_dates=...,
    columns: list[str] = ...,
    chunksize: int = ...,
    dtype_backend: DtypeBackend | lib.NoDefault = ...,
    dtype: DtypeArg | None = None,
) -> Iterator[DataFrame]: ...


def read_sql(
    sql,
    con,
    index_col: str | list[str] | None = None,
    coerce_float: bool = True,
    params=None,
    parse_dates=None,
    columns: list[str] | None = None,
    chunksize: int | None = None,
    dtype_backend: DtypeBackend | lib.NoDefault = lib.no_default,
    dtype: DtypeArg | None = None,
) -> DataFrame | Iterator[DataFrame]:
    """
    Read SQL query or database table into a DataFrame.

    This function is a convenience wrapper around ``read_sql_table`` and
    ``read_sql_query`` (for backward compatibility). It will delegate
    to the specific function depending on the provided input. A SQL query
    will be routed to ``read_sql_query``, while a database table name will
    be routed to ``read_sql_table``. Note that the delegated function might
    have more specific notes about their functionality not listed here.

    Parameters
    ----------
    sql : str or SQLAlchemy Selectable (select or text object)
        SQL query to be executed or a table name.
    con : ADBC Connection, SQLAlchemy connectable, str, or sqlite3 connection
        ADBC provides high performance I/O with native type support, where available.
        Using SQLAlchemy makes it possible to use any DB supported by that
        library. If a DBAPI2 object, only sqlite3 is supported. The user is responsible
        for engine disposal and connection closure for the ADBC connection and
        SQLAlchemy connectable; str connections are closed automatically. See
        `here <https://docs.sqlalchemy.org/en/20/core/connections.html>`_.
    index_col : str or list of str, optional, default: None
        Column(s) to set as index(MultiIndex).
    coerce_float : bool, default True
        Attempts to convert values of non-string, non-numeric objects (like
        decimal.Decimal) to floating point, useful for SQL result sets.
    params : list, tuple or dict, optional, default: None
        List of parameters to pass to execute method.  The syntax used
        to pass parameters is database driver dependent. Check your
        database driver documentation for which of the five syntax styles,
        described in PEP 249's paramstyle, is supported.
        Eg. for psycopg2, uses %(name)s so use params={'name' : 'value'}.
    parse_dates : list or dict, default: None
        - List of column names to parse as dates.
        - Dict of ``{column_name: format string}`` where format string is
          strftime compatible in case of parsing string times, or is one of
          (D, s, ns, ms, us) in case of parsing integer timestamps.
        - Dict of ``{column_name: arg dict}``, where the arg dict corresponds
          to the keyword arguments of :func:`pandas.to_datetime`
          Especially useful with databases without native Datetime support,
          such as SQLite.
    columns : list, default: None
        List of column names to select from SQL table (only used when reading
        a table).
    chunksize : int, default None
        If specified, return an iterator where `chunksize` is the
        number of rows to include in each chunk.
    dtype_backend : {'numpy_nullable', 'pyarrow'}
        Back-end data type applied to the resultant :class:`DataFrame`
        (still experimental). If not specified, the default behavior
        is to not use nullable data types. If specified, the behavior
        is as follows:

        * ``"numpy_nullable"``: returns nullable-dtype-backed :class:`DataFrame`
        * ``"pyarrow"``: returns pyarrow-backed nullable
          :class:`ArrowDtype` :class:`DataFrame`

        .. versionadded:: 2.0
    dtype : Type name or dict of columns
        Data type for data or columns. E.g. np.float64 or
        {'a': np.float64, 'b': np.int32, 'c': 'Int64'}.
        The argument is ignored if a table is passed instead of a query.

        .. versionadded:: 2.0.0

    Returns
    -------
    DataFrame or Iterator[DataFrame]
        Returns a DataFrame object that contains the result set of the
        executed SQL query or an SQL Table based on the provided input,
        in relation to the specified database connection.

    See Also
    --------
    read_sql_table : Read SQL database table into a DataFrame.
    read_sql_query : Read SQL query into a DataFrame.

    Notes
    -----
    ``pandas`` does not attempt to sanitize SQL statements;
    instead it simply forwards the statement you are executing
    to the underlying driver, which may or may not sanitize from there.
    Please refer to the underlying driver documentation for any details.
    Generally, be wary when accepting statements from arbitrary sources.

    Examples
    --------
    Read data from SQL via either a SQL query or a SQL tablename.
    When using a SQLite database only SQL queries are accepted,
    providing only the SQL tablename will result in an error.

    >>> from sqlite3 import connect
    >>> conn = connect(":memory:")
    >>> df = pd.DataFrame(
    ...     data=[[0, "10/11/12"], [1, "12/11/10"]],
    ...     columns=["int_column", "date_column"],
    ... )
    >>> df.to_sql(name="test_data", con=conn)
    2

    >>> pd.read_sql("SELECT int_column, date_column FROM test_data", conn)
       int_column date_column
    0           0    10/11/12
    1           1    12/11/10

    >>> pd.read_sql("test_data", "postgres:///db_name")  # doctest:+SKIP

    For parameterized query, using ``params`` is recommended over string interpolation.

    >>> from sqlalchemy import text
    >>> sql = text(
    ...     "SELECT int_column, date_column FROM test_data WHERE int_column=:int_val"
    ... )
    >>> pd.read_sql(sql, conn, params={"int_val": 1})  # doctest:+SKIP
       int_column date_column
    0           1    12/11/10

    Apply date parsing to columns through the ``parse_dates`` argument
    The ``parse_dates`` argument calls ``pd.to_datetime`` on the provided columns.
    Custom argument values for applying ``pd.to_datetime`` on a column are specified
    via a dictionary format:

    >>> pd.read_sql(
    ...     "SELECT int_column, date_column FROM test_data",
    ...     conn,
    ...     parse_dates={"date_column": {"format": "%d/%m/%y"}},
    ... )
       int_column date_column
    0           0  2012-11-10
    1           1  2010-11-12

    .. versionadded:: 2.2.0

       pandas now supports reading via ADBC drivers

    >>> from adbc_driver_postgresql import dbapi  # doctest:+SKIP
    >>> with dbapi.connect("postgres:///db_name") as conn:  # doctest:+SKIP
    ...     pd.read_sql("SELECT int_column FROM test_data", conn)
       int_column
    0           0
    1           1
    """

    check_dtype_backend(dtype_backend)
    if dtype_backend is lib.no_default:
        dtype_backend = "numpy"  # type: ignore[assignment]
    assert dtype_backend is not lib.no_default

    with pandasSQL_builder(con) as pandas_sql:
        if isinstance(pandas_sql, SQLiteDatabase):
            return pandas_sql.read_query(
                sql,
                index_col=index_col,
                params=params,
                coerce_float=coerce_float,
                parse_dates=parse_dates,
                chunksize=chunksize,
                dtype_backend=dtype_backend,
                dtype=dtype,
            )

        try:
            _is_table_name = pandas_sql.has_table(sql)
        except Exception:
            # using generic exception to catch errors from sql drivers (GH24988)
            _is_table_name = False

        if _is_table_name:
            return pandas_sql.read_table(
                sql,
                index_col=index_col,
                coerce_float=coerce_float,
                parse_dates=parse_dates,
                columns=columns,
                chunksize=chunksize,
                dtype_backend=dtype_backend,
            )
        else:
            return pandas_sql.read_query(
                sql,
                index_col=index_col,
                params=params,
                coerce_float=coerce_float,
                parse_dates=parse_dates,
                chunksize=chunksize,
                dtype_backend=dtype_backend,
                dtype=dtype,
            )

