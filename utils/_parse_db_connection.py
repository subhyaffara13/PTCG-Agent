
def _parse_db_connection(
    data: Mapping[str, Any], config: tiering_service_pb2.ServerConfig
) -> None:
  """Parses database connection string into ServerConfig."""
  if "db_connection_str" in data:
    config.db_connection_str = str(data["db_connection_str"])

