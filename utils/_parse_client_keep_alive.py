
def _parse_client_keep_alive(
    data: Mapping[str, Any], config: tiering_service_pb2.ServerConfig
) -> None:
  """Parses client keep-alive interval into ServerConfig."""
  if "client_keep_alive_interval_seconds" in data:
    config.client_keep_alive_interval_seconds = int(
        data["client_keep_alive_interval_seconds"]
    )
  elif "client_keep_alive_interval" in data:
    val = data["client_keep_alive_interval"]
    if isinstance(val, (int, float)):
      config.client_keep_alive_interval_seconds = int(val)
    else:
      timedelta_val = _parse_timedelta(str(val))
      config.client_keep_alive_interval_seconds = int(
          timedelta_val.total_seconds()
      )

