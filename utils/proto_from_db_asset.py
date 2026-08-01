
def proto_from_db_asset(db_asset: db_schema.Asset) -> tiering_service_pb2.Asset:
  """Converts a db_schema.Asset to a tiering_service_pb2.Asset.

  Maps database fields, including relationships (tier paths) and timestamps,
  to the protobuf Asset representation.

  Args:
    db_asset: The database Asset model instance.

  Returns:
    The constructed protobuf Asset message.
  """
  proto_asset = tiering_service_pb2.Asset(
      uuid=db_asset.asset_uuid,
      path=db_asset.path,
      user=db_asset.user,
      tags=db_asset.tags if db_asset.tags else [],
      state=db_asset.state.value,
      tier_paths=(
          _proto_from_db_tier_path(tier_path)
          for tier_path in db_asset.tier_paths
      ),
  )

  if db_asset.created_at:
    proto_asset.created_at.FromDatetime(db_asset.created_at)
  if db_asset.finalized_at:
    proto_asset.finalized_at.FromDatetime(db_asset.finalized_at)
  if db_asset.deleted_at:
    proto_asset.deleted_at.FromDatetime(db_asset.deleted_at)
  if db_asset.updated_at:
    proto_asset.updated_at.FromDatetime(db_asset.updated_at)

  return proto_asset

