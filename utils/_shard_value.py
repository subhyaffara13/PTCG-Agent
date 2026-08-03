import math


def _shard_value(val: TfVal,
                 sd: xla_client.HloSharding | None, *,
                 skip_replicated_sharding: bool) -> TfVal:
  """Apply sharding to a TfVal."""
  if sd is None:
    return val

  sharding_proto = sd.to_proto()
  if (skip_replicated_sharding and
      op_shardings.is_hlo_sharding_replicated(sd)):
    return val

  # Tensorflow heavily relies on tile_assignment_devices proto fields specific
  # to V1 sharding format, falling back to this format.
  if (
      not sharding_proto.tile_assignment_devices
      and sharding_proto.iota_reshape_dims
  ):
    tad = list(
        np.arange(math.prod(sharding_proto.tile_assignment_dimensions))
        .reshape(sharding_proto.iota_reshape_dims)
        .transpose(sharding_proto.iota_transpose_perm)
        .flat
    )
  else:
    tad = sharding_proto.tile_assignment_devices

  # To use xla_sharding.py, we must have a xla_data_pb2.OpSharding.
  xla_sharding_v1_proto: xla_data_pb2.OpSharding = xla_data_pb2.OpSharding(
      type=int(sharding_proto.type),  # pyrefly: ignore [bad-argument-type]
      tile_assignment_dimensions=sharding_proto.tile_assignment_dimensions,
      tile_assignment_devices=tad,  # pyrefly: ignore [bad-argument-type]
      replicate_on_last_tile_dim=sharding_proto.replicate_on_last_tile_dim,
      last_tile_dims=sharding_proto.last_tile_dims,  # pyrefly: ignore [bad-argument-type]
  )
  # Shardy requires V2 sharding format.
  if config.use_shardy_partitioner.value:
    xla_sharding_v2_proto: xla_data_pb2.OpSharding = xla_data_pb2.OpSharding(
        type=int(sharding_proto.type),  # pyrefly: ignore [bad-argument-type]
        tile_assignment_dimensions=sharding_proto.tile_assignment_dimensions,
        tile_assignment_devices=sharding_proto.tile_assignment_devices,
        iota_reshape_dims=sharding_proto.iota_reshape_dims,
        iota_transpose_perm=sharding_proto.iota_transpose_perm,
        replicate_on_last_tile_dim=sharding_proto.replicate_on_last_tile_dim,
        last_tile_dims=sharding_proto.last_tile_dims,  # pyrefly: ignore [bad-argument-type]
    )
  else:
    xla_sharding_v2_proto = None  # pyrefly: ignore [bad-assignment]
  if tf_context.executing_eagerly():
    raise ValueError(
        "A jit function with sharded arguments or results must be used under a `tf.function` context. "
        "See https://github.com/jax-ml/jax/blob/main/jax/experimental/jax2tf/README.md#support-for-partitioning for a discussion")

  tf_version = tuple(int(v) for v in tf.__version__.split(".")[:2])
  # apply_to_tensor comes from a tensorflow package, check the tensorflow
  # version to make sure that it has the sharding_v2_proto parameter.
  if tf_version < (2, 20):
    return xla_sharding.Sharding(proto=xla_sharding_v1_proto).apply_to_tensor(
        val, use_sharding_op=True
    )
  return xla_sharding.Sharding(proto=xla_sharding_v1_proto).apply_to_tensor(
      val, use_sharding_op=True, sharding_v2_proto=xla_sharding_v2_proto
  )

