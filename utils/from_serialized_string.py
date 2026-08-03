import json

def from_serialized_string(serialized_str) -> ShardingMetadata:
  """Converts `serialized_string` to `ShardingMetadata`."""
  deserialized_dict = json.loads(serialized_str)
  if deserialized_dict[_SHARDING_TYPE] == ShardingTypes.NAMED_SHARDING.value:
    return NamedShardingMetadata.from_deserialized_dict(deserialized_dict)
  elif (
      deserialized_dict[_SHARDING_TYPE]
      == ShardingTypes.SINGLE_DEVICE_SHARDING.value
  ):
    return SingleDeviceShardingMetadata.from_deserialized_dict(
        deserialized_dict
    )
  elif (
      deserialized_dict[_SHARDING_TYPE]
      == ShardingTypes.POSITIONAL_SHARDING.value
  ):
    raise ValueError(
        'jax.sharding.PositionalSharding has been deprecated. Please use'
        ' jax.NamedSharding instead.')
  else:
    raise NotImplementedError(
        f'Conversion for {deserialized_dict[_SHARDING_TYPE]} has not been'
        ' implemented.'
    )

