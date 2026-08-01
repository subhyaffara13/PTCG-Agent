
def _parse_storage_backends(
    data: Mapping[str, Any], config: tiering_service_pb2.ServerConfig
) -> None:
  """Parses storage backends list into ServerConfig."""
  backends_data = data.get("storage_backends", [])
  for b_data in backends_data:
    backend = config.storage_backends.add()
    _parse_storage_backend(b_data, backend)

