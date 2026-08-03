from typing import Any

def execute_raw_sql_query(sql_query: str, *, token: str | bool | None = None) -> list[dict[str, Any]]:
    normalized_query = sql_query.strip().rstrip(";").strip()
    _raise_on_forbidden_query(normalized_query)

    connection = None
    try:
        connection = _get_duckdb_connection(token=token)
        relation = connection.sql(normalized_query)
        if relation is None:
            raise ValueError("SQL query must return rows.")

        if isinstance(relation, _DuckDBCliRelation):
            # DuckDB binary => run CLI => parse JSON
            return relation.execute()
        else:
            # DuckDB Python API => fetch columns + rows => convert to dicts
            columns = tuple(column[0] for column in relation.description)
            rows = tuple(tuple(row) for row in relation.fetchall())
            return [dict(zip(columns, row)) for row in rows]
    finally:
        if connection is not None:
            connection.close()

