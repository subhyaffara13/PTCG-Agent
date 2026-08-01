
def _construct_deserialization_param(
    info: types_v0.ParamInfo,
    restore_args: types_v0.RestoreArgs,
) -> types.DeserializationParam[
    types.AbstractShardedArray
    | types.AbstractArray
    | Type[types.AbstractArray]
    | types.AbstractScalar
    | Type[types.AbstractScalar]
    | types.AbstractString
    | Type[types.AbstractString]
    | None
]:
  """Constructs a :py:class:`~.v1.serialization.DeserializationParam` from a ParamInfo and :py:class:`~orbax.checkpoint.type_handlers.RestoreArgs`."""

  logging.vlog(1, 'compatibility.py: restore_args: %s', restore_args)

  if restore_args.restore_type == np.ndarray:
    # NumPy type
    value = numpy_leaf_handler.NumpyShapeDtype(
        dtype=restore_args.dtype,
        shape=None,
    )
  elif isinstance(restore_args.restore_type, type) and issubclass(
      restore_args.restore_type, get_args(scalar_leaf_handler.Scalar)
  ):
    # Scalar type
    logging.vlog(1, 'Scalar restore_type set to: %s', restore_args.restore_type)
    value = restore_args.restore_type
  elif isinstance(restore_args, type_handlers_v0.ArrayRestoreArgs):
    # JAX Array type, construct value as `jax.ShapeDtypeStruct`.
    arg = cast(type_handlers_v0.ArrayRestoreArgs, restore_args)

    logging.info(
        'name: %s, ArrayRestoreArgs: %s, write_shape: %s',
        info.name,
        arg,
        info.write_shape,
    )

    if arg.mesh is not None and arg.mesh_axes is not None:
      sharding = jax.sharding.NamedSharding(arg.mesh, arg.mesh_axes)
    elif arg.sharding is not None:
      if isinstance(arg.sharding, sharding_metadata.ShardingMetadata):
        sharding = arg.sharding.to_jax_sharding()
      else:
        sharding = arg.sharding
    else:
      sharding = None

    # Restore as jax.Array regardless of whether sharding is None.
    value = jax.ShapeDtypeStruct(arg.shape, arg.dtype, sharding=sharding)
  elif info.write_shape is not None:
    # TODO(dnlng): this is needed due to write_shape is passed into the
    # metadata() call, and then returned metadata will include this write_shape
    # in it. We should refractor how this write_shape is populated from the v0
    # so that the compatibility wrapper doesn't only work specific for
    # ArrayLeafHandler.
    value = array_leaf_handler.ArrayMetadata(
        shape=None,
        dtype=None,
        sharding_metadata=None,
        storage_metadata=value_metadata.StorageMetadata(
            chunk_shape=None,
            write_shape=info.write_shape,
        ),
    )
    logging.vlog(1, 'ArrayMetadata as param.value: %s', value)
  elif (
      restore_args.restore_type in (None, int, float)
      or isinstance(restore_args.restore_type, (np.dtype, jnp.dtype))
      or issubclass(restore_args.restore_type, np.number)
  ):
    # scalar type
    value = restore_args.restore_type
  elif issubclass(restore_args.restore_type, str):
    # string type
    value = str
  else:
    raise ValueError(
        'Unsupported restore_args: %s. Cannot construct DeserializationParam.'
        % restore_args
    )

  logging.vlog(1, 'deserialization_param.value: %r', value)

  return types.DeserializationParam(
      keypath=info.keypath
      if info.keypath is not None
      else _keypath_from_param_name(info.name),
      value=value,
  )

