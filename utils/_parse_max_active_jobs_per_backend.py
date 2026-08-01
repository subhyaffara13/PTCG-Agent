
def _parse_max_active_jobs_per_backend(
    data: Mapping[str, Any], config: tiering_service_pb2.ServerConfig
) -> None:
  """Parses max active jobs per backend into ServerConfig."""
  if "max_active_jobs_per_backend" in data:
    config.max_active_jobs_per_backend = int(
        data["max_active_jobs_per_backend"]
    )

