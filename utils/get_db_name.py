
def get_db_name(database: Union["SyncDatabase", "AsyncDatabase"]):
    """
    Get a short string representation of a database for observability.

    Args:
        database: Database instance

    Returns:
        Short database name in format "{host}:{port}/{weight}"
    """

    host = database.client.get_connection_kwargs()["host"]
    port = database.client.get_connection_kwargs()["port"]
    weight = database.weight

    return f"{host}:{port}/{weight}"

