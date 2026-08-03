from typing import Union

def _get_duckdb_connection(
    token: str | bool | None,
) -> Union["duckdb.DuckDBPyConnection", "_DuckDBCliConnection"]:
    try:
        # If DuckDB is installed as a Python package, use it!
        import duckdb
    except ImportError as error:
        # Otherwise, use the DuckDB CLI binary.
        duckdb_binary = shutil.which("duckdb")
        if duckdb_binary is None:
            raise ImportError(
                "DuckDB is required for `hf datasets sql`. Install the Python package with `pip install duckdb` or "
                "install the DuckDB CLI binary (for example `brew install duckdb`)."
            ) from error
        return _DuckDBCliConnection(binary_path=duckdb_binary, token=token)

    # Create a new connection (Python API).
    connection = duckdb.connect()
    try:
        for statement in _build_duckdb_secret_statements(token):
            connection.execute(statement)
        return connection
    except Exception:
        connection.close()
        raise

