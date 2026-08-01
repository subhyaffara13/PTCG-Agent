
def construct_restore_args(
    target: PyTree,
    sharding_tree: Optional[PyTree] = None,
    set_global_shape: bool = True,
    support_layout: bool = False,
    strict: bool = True,
) -> PyTree:
  """Creates restore_args given a target PyTree.

  This method should be used in conjunction with a CheckpointManager or
  Checkpointer that wraps a PyTreeCheckpointHandler.

  For example::

    mngr = CheckpointManager(path, Checkpointer(PyTreeCheckpointHandler()))
    restore_args = construct_restore_args(train_state, train_state_sharding)
    restore_kwargs = {'restore_args': restore_args}
    mngr.restore(..., restore_kwargs=restore_kwargs)

  OR::

    mngr = CheckpointManager(path, {
        'train_state': Checkpointer(PyTreeCheckpointHandler())
    })
    restore_args = construct_restore_args(train_state, train_state_sharding)
    restore_kwargs = {'train_state': {'restore_args': restore_args} }
    mngr.restore(..., restore_kwargs=restore_kwargs)

  OR::

    ckptr = Checkpointer(PyTreeCheckpointHandler())
    restore_args = construct_restore_args(train_state, train_state_sharding)
    ckptr.restore(..., restore_args=restore_args)

  If a leaf in target is a np.ndarray, or int, or string, for example, a
  corresponding value for that leaf must be provided in axes_tree, but will be
  ignored.

  Args:
    target: The returned PyTree will match the structure of `target`. `target`
      may contain `value_metadata.Metadata`, real scalar or array values, or may
      contain jax.ShapeDtypeStruct.
    sharding_tree: A PyTree matching `target` which will be used to set the
      restoration sharding. If not provided, sharding will default to the
      shardings specified by `target`.
    set_global_shape: If true, set the `global_shape` field of ArrayRestoreArgs.
    support_layout: If true, layout is extracted from jax.Array or
      jax.ShapeDtypeStruct.
    strict: If False, allow padding/slicing for uneven sharding.

  Returns:
    A PyTree matching target of RestoreArgs (or ArrayRestoreArgs) objects.
  """

  def _array_restore_args(
      value: Any,
      sharding: Optional[jax.sharding.Sharding | Format],  # pytype: disable=unsupported-operands
      dtype: Optional[np.dtype] = None,
  ) -> type_handlers.ArrayRestoreArgs:
    global_shape = None
    # For random keys, we only allow overriding the sharding.
    if set_global_shape and not jax.dtypes.issubdtype(
        value.dtype, jax.dtypes.prng_key
    ):
      global_shape = value.shape
    return type_handlers.ArrayRestoreArgs(
        restore_type=jax.Array,
        sharding=sharding,
        global_shape=global_shape,
        dtype=dtype,
        strict=strict,
    )

  def _restore_args(
      value: Any,
      sharding: Optional[jax.sharding.Sharding],
  ) -> type_handlers.RestoreArgs:
    if isinstance(value, jax.ShapeDtypeStruct):
      if sharding is None:
        return type_handlers.RestoreArgs(
            restore_type=np.ndarray, dtype=value.dtype
        )
      else:
        return _array_restore_args(value, sharding, value.dtype)
    elif isinstance(value, value_metadata.Metadata):
      if isinstance(value, value_metadata.StringMetadata):
        return type_handlers.RestoreArgs(restore_type=str)
      elif isinstance(value, value_metadata.ScalarMetadata):
        return type_handlers.RestoreArgs(
            restore_type=_python_type_from_dtype(value.dtype), dtype=value.dtype
        )
      elif isinstance(value, value_metadata.ArrayMetadata):
        if sharding is None:
          return type_handlers.RestoreArgs(
              restore_type=np.ndarray, dtype=value.dtype
          )
        else:
          return _array_restore_args(value, sharding, value.dtype)
      else:
        raise ValueError(f'Unsupported value_metadata class: {type(value)}.')
    elif isinstance(value, STANDARD_ARRAY_TYPES):
      if isinstance(value, np.ndarray):
        return type_handlers.RestoreArgs(
            restore_type=type(value), dtype=value.dtype
        )
      elif isinstance(value, jax.Array):
        return _array_restore_args(value, sharding, value.dtype)
      else:
        return type_handlers.RestoreArgs(restore_type=type(value))
    elif isinstance(value, str):
      return type_handlers.RestoreArgs(restore_type=str)
    elif type_handlers.is_placeholder(value):
      return type_handlers.RestoreArgs(restore_type=type(PLACEHOLDER))
    else:
      raise ValueError(f'Unsupported type: {type(value)}')

  def _get_sharding_or_layout(value):
    return arrays_sharding_lib.get_sharding_or_format(
        value, support_format=support_layout
    )

  def _return_key_data(value):
    # replace jax.random.key with underneath jax.Array
    if isinstance(value, jax.Array) and jax.dtypes.issubdtype(
        value.dtype, jax.dtypes.prng_key
    ):
      # For random keys, extract the dtype and shape as a regular Jax array.
      # Stored metadata will help restoring the original random key.
      return jax.random.key_data(value)
    return value

  target = jax.tree.map(_return_key_data, target)

  if sharding_tree is None:
    sharding_tree = jax.tree.map(_get_sharding_or_layout, target)
  if isinstance(target, tree_metadata.TreeMetadata):
    return tree_metadata.build_default_tree_metadata(
        jax.tree.map(_restore_args, target.tree, sharding_tree.tree),
        custom_metadata=target.custom_metadata,
    )
  else:
    return jax.tree.map(_restore_args, target, sharding_tree)

