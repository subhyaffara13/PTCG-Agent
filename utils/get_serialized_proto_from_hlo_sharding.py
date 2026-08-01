
def get_serialized_proto_from_hlo_sharding(
    sharding: xla_client.HloSharding) -> bytes:
  return sharding.to_proto().SerializeToString()

