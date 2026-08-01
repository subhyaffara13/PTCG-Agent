
def _parse_service_account(
    data: Mapping[str, Any], config: tiering_service_pb2.ServerConfig
) -> None:
  """Parses service_account into ServerConfig."""
  if "service_account" in data and data["service_account"] is not None:
    config.service_account = str(data["service_account"])

