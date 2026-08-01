
def _serialize_sharding(
    builder: flatbuffers.Builder, s: _export.NamedSharding | None, *,
    uniques: _SerializedUniques) -> int:
  named_sharding = None

  if s is not None:
    named_sharding = _serialize_named_sharding(builder, s, uniques=uniques)

  ser_flatbuf.ShardingStart(builder)
  if named_sharding is not None:
    ser_flatbuf.ShardingAddNamedSharding(builder, named_sharding)
  return ser_flatbuf.ShardingEnd(builder)

