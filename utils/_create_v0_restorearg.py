
def _create_v0_restorearg(
    param: ArrayDeserializationParam,
    context: context_lib.Context,
) -> type_handlers_v0.ArrayRestoreArgs:
  """Creates a V0 `ArrayRestoreArgs` from V1 params."""
  restore_arg_cls = (
      type_handlers_v0.SingleReplicaArrayRestoreArgs
      if context.array_options.loading.use_load_and_broadcast
      else type_handlers_v0.ArrayRestoreArgs
  )
  value = param.value
  if value is None or isinstance(value, type):
    return restore_arg_cls(restore_type=jax.Array)
  elif protocol_utils.is_subclass_protocol(value, AbstractShardedArray):
    value = typing.cast(AbstractShardedArray, value)
    return restore_arg_cls(
        restore_type=jax.Array,
        dtype=value.dtype,
        sharding=value.sharding,
        shape=value.shape,
        strict=not context.array_options.loading.enable_padding_and_truncation,
    )
  else:
    raise TypeError(f'Unrecognized abstract value type: {type(value)}')


def _create_v0_restorearg(
    param: NumpyDeserializationParam,
) -> type_handlers_v0.RestoreArgs:
  """Creates a V0 `RestoreArgs` from V1 params."""

  value = param.value
  if value is None or isinstance(value, type):
    return type_handlers_v0.RestoreArgs(
        restore_type=np.ndarray,
    )
  else:
    value = typing.cast(types.AbstractArray, value)
    logging.vlog(1, 'name: %s, v.dtype: %s', param.name, value.dtype)
    return type_handlers_v0.RestoreArgs(
        restore_type=np.ndarray,
        dtype=value.dtype,
    )


def _create_v0_restorearg(
    param: ScalarDeserializationParam,
) -> type_handlers_v0.RestoreArgs:
  """Creates a V0 RestoreArgs from V1 params."""
  if isinstance(param.value, Scalar):
    # users pass values direclty
    restore_type = type(param.value)
  else:
    restore_type = param.value

  logging.vlog(1, "setting restore_type: %r", restore_type)
  return type_handlers_v0.RestoreArgs(
      restore_type=restore_type,
  )

