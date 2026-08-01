
def datasets_sql(
    sql: Annotated[str, typer.Argument(help="Raw SQL query to execute.")],
    token: TokenOpt = None,
) -> None:
    """Execute a raw SQL query with DuckDB against dataset parquet URLs."""
    try:
        result = execute_raw_sql_query(sql_query=sql, token=token)
    except ImportError as e:
        raise CLIError(str(e)) from e
    out.table(result)

