from typing import Any

def _parse_storage_backend(
    b_data: Mapping[str, Any],
    backend: tiering_service_pb2.StorageBackend,
) -> None:
  """Parses a dictionary into a StorageBackend proto."""
  if "level" in b_data and b_data["level"] is not None:
    backend.level = int(b_data["level"])
  else:
    raise ValueError(
        "StorageBackend configuration missing required key: 'level'"
    )

  if "backend_type" in b_data and b_data["backend_type"]:
    b_type = b_data["backend_type"]
    if isinstance(b_type, str):
      b_type_upper = b_type.upper()
      if b_type_upper in ("LUSTRE", "BACKEND_TYPE_LUSTRE"):
        backend.backend_type = tiering_service_pb2.BACKEND_TYPE_LUSTRE
      elif b_type_upper in ("GCS", "BACKEND_TYPE_GCS"):
        backend.backend_type = tiering_service_pb2.BACKEND_TYPE_GCS
      else:
        raise ValueError(f"Unknown storage backend_type: {b_type}")
    else:
      backend.backend_type = b_type
  else:
    raise ValueError(
        "StorageBackend configuration missing required key: 'backend_type'"
    )

  if "prefix" in b_data and b_data["prefix"] is not None:
    backend.prefix = str(b_data["prefix"])
  else:
    raise ValueError(
        "StorageBackend configuration missing required key: 'prefix'"
    )

  if "zone" in b_data and b_data["zone"]:
    backend.zone = str(b_data["zone"])
  elif "region" in b_data and b_data["region"]:
    backend.region = str(b_data["region"])
  elif "multi_regions" in b_data and b_data["multi_regions"]:
    mr = b_data["multi_regions"]
    if isinstance(mr, dict) and "regions" in mr:
      backend.multi_regions.regions.extend(mr["regions"])
    elif isinstance(mr, (list, tuple)):
      backend.multi_regions.regions.extend(mr)
    else:
      raise ValueError(f"Invalid multi_regions format: {mr}")

