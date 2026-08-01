
def load_checkpointables(
    path: path_types.PathLike,
    abstract_checkpointables: (
        dict[str, AbstractCheckpointable]
        | CheckpointMetadata[dict[str, AbstractCheckpointable]]
        | None
    ) = None,
) -> dict[str, Checkpointable]:
  """Loads checkpointables.

  See documentation for :py:func:`.save_checkpointables` for more context on
  what a checkpointable is.

  This function can be used to load any checkpoint saved by
  :py:func:`.save_checkpointables` (or :py:func:`.save`). The path should
  contain a number of subdirectories - each of these represents the name of a
  checkpointable.

  This function must be called on all available controller processes.

  The operation blocks until complete. For improved performance, consider using
  :py:func:`.load_checkpointables_async` instead.

  If `abstract_checkpointables` is not provided, the checkpointables will be
  loaded exactly as saved.

  IMPORTANT: Loading is more brittle and error-prone when not providing
  `abstract_checkpointables`. Always provide `abstract_checkpointables` if
  possible. Note that you can always obtain the information about the
  checkpointables using
  :py:func:`.checkpointables_metadata`.

  If `abstract_checkpointables` is provided, the value provided for each key
  is treated as the abstract type for the given checkpointable. For example, for
  a `PyTree` of `jax.Array`, the corresponding abstract checkpointable is a
  `PyTree` of `jax.ShapeDtypeStruct`. `None` is always a valid abstract
  checkpointable, which just indicates that the checkpointable should be loaded
  exactly as saved.

  The keys provided in `abstract_checkpointables` may be any subset of the
  checkpointables in the checkpoint. Any checkpointables names not provided in
  `abstract_checkpointables` will not be loaded.

  Example Usage:

    Load checkpointables from a saved checkpoint::

      path = '/tmp/my_checkpoint_step_100'

      # Save multiple components (checkpointables)
      params = {'w': jnp.ones((8, 8)), 'b': jnp.zeros(8)}
      opt_state = {'count': jnp.array(100)}

      # Setup Grain (Stateful Checkpointable)
      import grain
      dataset_iter = iter(
          grain.MapDataset.range(30)
          .batch(3)
          .map(lambda x: x.tolist())
      )

      ocp.save_checkpointables(path, {
          'model': params,
          'optimizer': opt_state,
          'dataset': dataset_iter,
      })

      # Load the checkpointables
      abstract_params = jax.eval_shape(lambda: params)
      abstract_opt = jax.eval_shape(lambda: opt_state)

      abstract_checkpointables = {
          'model': abstract_params,
          'optimizer': abstract_opt,
          # Dataset is restored statefully. An initialized object must be
          # passed, but its position will be set to the position recorded in the
          # checkpoint after restoring.
          'dataset': dataset_iter,
      }

      # Load all components
      restored = ocp.load_checkpointables(path, abstract_checkpointables)

      # Load only a subset
      restored_subset = ocp.load_checkpointables(
          path,
          {'model': abstract_params}
      )

  Args:
    path: The path to load the checkpoint from. This path must contain a
      subdirectory for each checkpointable.
    abstract_checkpointables: A dictionary of abstract checkpointables.
      Dictionary keys represent the names of the checkpointables, while the
      values are the abstract checkpointable objects themselves.

  Returns:
    A dictionary of checkpointables. Dictionary keys represent the names of the
    checkpointables, while the values are the checkpointable objects themselves.

  Raises:
    FileNotFoundError: If the checkpoint path does not exist.
  """
  start_time = time.time()
  event_tracking.OperationRecorder(
      path,
      operation_type=event_tracking.OperationType.LOAD,
      async_origin=False,
  ).record_start(start_time)

  abstract_checkpointables = _standardize_abstract_checkpointables(
      abstract_checkpointables
  )
  validation.validate_abstract_checkpointables(abstract_checkpointables)

  ctx = context_lib.get_context()
  path = ctx.file_options.path_class(path)
  layout = asyncio_utils.run_sync(
      layout_registry.get_checkpoint_layout(path, ctx.checkpoint_layout)
  )

  return _load_impl(
      path,
      functools.partial(
          layout.load_checkpointables,
          path=path,
          abstract_checkpointables=abstract_checkpointables,
      ),
      start_time=start_time,
  )

