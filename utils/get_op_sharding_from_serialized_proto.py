
def get_op_sharding_from_serialized_proto(
    sharding: bytes) -> xla_client.OpSharding:
  proto = xla_client.OpSharding()
  proto.ParseFromString(sharding)
  return proto

