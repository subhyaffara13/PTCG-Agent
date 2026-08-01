
def get_hlo_sharding_from_serialized_proto(
    sharding: bytes) -> xla_client.HloSharding:
  return xla_client.HloSharding.from_proto(
      get_op_sharding_from_serialized_proto(sharding))

