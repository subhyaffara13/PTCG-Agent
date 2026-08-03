from typing import Any

def _parse_gcp_project(
    data: Mapping[str, Any], config: tiering_service_pb2.ServerConfig
) -> None:
  """Parses gcp_project into ServerConfig."""
  if "gcp_project" in data and data["gcp_project"] is not None:
    config.gcp_project = str(data["gcp_project"])

