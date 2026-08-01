
def _proto_from_db_tier_path(
    tier_path: db_schema.TierPath,
) -> tiering_service_pb2.TierPath:
  """Converts a db_schema.TierPath to a tiering_service_pb2.TierPath.

  Extracts storage backend details and timestamps from the database model
  and constructs the corresponding protobuf message.

  Args:
    tier_path: The database TierPath model instance.

  Returns:
    The constructed protobuf TierPath message.
  """
  storage_backend = tier_path.storage_backend

  def _get_location_kwargs(sb: db_schema.StorageBackend):
    if sb.zone is not None:
      return {"zone": sb.zone}
    if sb.region is not None:
      return {"region": sb.region}
    if sb.multi_regions is not None:
      return {
          "multi_regions": tiering_service_pb2.MultipleRegions(
              regions=sb.multi_regions
          )
      }
    return {}

  storage_backend_kwargs = {
      "id": storage_backend.id,
      "level": storage_backend.level,
      "backend_type": storage_backend.backend_type.value,
      "prefix": storage_backend.prefix,
      **_get_location_kwargs(storage_backend),
  }

  proto_storage_backend = tiering_service_pb2.StorageBackend(
      **storage_backend_kwargs
  )

  ready_at_pb = None
  if tier_path.ready_at is not None:
    ready_at_pb = timestamp_pb2.Timestamp()
    ready_at_pb.FromDatetime(tier_path.ready_at)

  expires_at_pb = None
  if tier_path.expires_at is not None:
    expires_at_pb = timestamp_pb2.Timestamp()
    expires_at_pb.FromDatetime(tier_path.expires_at)

  return tiering_service_pb2.TierPath(
      id=tier_path.id,
      path=tier_path.path,
      storage_backend=proto_storage_backend,
      ready_at=ready_at_pb,
      expires_at=expires_at_pb,
      tier_path_uuid=tier_path.tier_path_uuid,
  )

