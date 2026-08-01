
def _deserialize_sharding(s: ser_flatbuf.Sharding, *,
                          uniques: _SerializedUniques) -> _export.HloSharding | named_sharding.NamedSharding | None:
  if (named_sharding_off := s.NamedSharding()) is not None:
    # After 1/15/26 all exports will have named shardings (or None)
    # TODO(necula): We must keep reading the NamedSharding for 6 months after 4/4/26
    return _deserialize_named_sharding(named_sharding_off, uniques=uniques)

  # TODO(b/489569164): We must keep reading the HloSharding for 6 months after 1/15/2026.
  if not s.HloShardingProtoIsNone():
    proto = xla_client.OpSharding()
    proto.ParseFromString(s.HloShardingProtoAsNumpy().tobytes())
    return xla_client.HloSharding.from_proto(proto)

  return None  # Unspecified sharding

