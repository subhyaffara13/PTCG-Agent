
def save_async(
    path: path_types.PathLike,
    state: tree_types.PyTreeOf[tree_types.Leaf],
    *,
    custom_metadata: tree_types.JsonType | None = None,
) -> async_types.AsyncResponse[None]:
  """Partially saves a PyTree asynchronously.

  Unlike :py:func:`.save`, this function returns an
  :py:class:`.AsyncResponse`
  immediately after scheduling the save operation. The actual writing to disk
  happens in a background thread. You can use `response.result()` to block
  until the operation is complete.

  This function allows for incrementally updating a checkpoint. It is designed
  to be called multiple times. The first call initiates a new partial save
  "session" in a temporary location. Subsequent calls will update this session
  by creating a new version that includes all previous changes plus the new
  ones.

  The operation is atomic; if it is interrupted, the previous version of the
  partial save will be preserved.

  IMPORTANT: The checkpoint is not finalized at the target `path` until
  :py:func:`.finalize` is called. The intermediate checkpoints are
  temporary and may be garbage collected in certain environments.

  ### Workflow

  A typical partial save workflow involves one or more calls to
  :py:func:`.save_async` followed by a single call to
  :py:func:`.finalize`::

    path = '/path/to/my/checkpoint'

    # The first call creates a temporary directory and returns immediately.
    response1 = ocp.partial.save_async(path, {'layer1': ..., 'step': 1})

    # A subsequent call also returns immediately. Orbax ensures that this
    # operation waits for the first one to complete before starting.
    response2 = ocp.partial.save_async(
        path, {'layer2': ..., 'metrics': ...}
    )

    # Wait for all async partial saves to complete before finalizing.
    response1.result()
    response2.result()

    # This call commits the latest version to the final destination at
    # '/path/to/my/checkpoint'.
    ocp.partial.finalize(path)

  ### Additions vs. Replacements

  The provided `state` represents a set of updates.
  - If a key in `state` (e.g., 'metrics') does not exist in the on-disk
    checkpoint, it is treated as an **addition**.
  - If a key (e.g., 'step') already exists, its value is **replaced**.
    Replacements are currently NOT supported. Please reach out to the Orbax team
    if you need this functionality.

  See :py:func:`~.v1.save_async` for general
  PyTree saving documentation.

  Args:
    path: The path to save the checkpoint to.
    state: The PyTree to save. This may be any JAX PyTree consisting of
      supported leaf types (see :py:class:`~.v1.tree.Leaf`).
      Default supported leaf types include `jax.Array`, `np.ndarray`,
      simple types like `int`, `float`, `str`, and empty nodes.
    custom_metadata: User-provided custom metadata. An arbitrary
      JSON-serializable dictionary the user can use to store additional
      information. The field is treated as opaque by Orbax.

  Returns:
    An :py:class:`.AsyncResponse` that can be used to block until the save is
    complete.
    Blocking can be done using `response.result()`, which returns `None`.

  Raises:
    FileExistsError: If a finalized checkpoint already exists at `path`. To
      overwrite, it must be deleted first.
  """
  ctx = context_lib.get_context()
  path = ctx.file_options.path_class(path)
  if path.exists():
    raise FileExistsError(f'Finalized checkpoint already exists at {path}.')

  return execution.save_checkpointables_impl(
      partial_path_lib.add_partial_save_suffix(path),
      {STATE_CHECKPOINTABLE_KEY: _PartialSavePyTree(state)},
      overwrite=False,
      custom_metadata=custom_metadata,
      async_origin=True,
      partial_save=True,
  )


def save_async(
    path: path_types.PathLike,
    state: tree_types.PyTreeOf[tree_types.Leaf],
    *,
    checkpointable_name: str = STATE_CHECKPOINTABLE_KEY,
    overwrite: bool = False,
    custom_metadata: tree_types.JsonType | None = None,
) -> async_types.AsyncResponse[None]:
  """Saves a `PyTree` asynchronously.

  Unlike :py:func:`.save`, this function returns immediately after the
  save operation is scheduled
  (except for certain operations, like device-to-host copying of on-device
  arrays, which must happen on the main thread). Further writing operations
  continue in a background thread. An
  :py:class:`~.AsyncResponse`
  is returned that can be used to block until the save is complete (using
  `response.result()`). Make sure to wait for completion before attempting to
  load the checkpoint or exiting the program. This function should be called on
  all available controller processes.


  Example usage:
    Simple save of a dictionary containing JAX arrays asynchronously::

      state = {
          'params': {
              'w': jnp.ones((8, 8)),
              'b': jnp.zeros(8),
          },
          'step': 100
      }
      # Saves to /tmp/my_checkpoint/
      future = ocp.experimental.v1.save_async(
          '/tmp/my_checkpoint', state
      )

      # Perform other work here...

      # Wait for completion only when necessary
      future.result()

  Args:
    path: The path to save the checkpoint to.
    state: The `PyTree` to save. This may be any JAX `PyTree` (including custom
      objects registered as `PyTrees`) consisting of supported leaf types. See
      `orbax.checkpoint.v1.tree` for a table of standard supported leaf types.
    checkpointable_name: The name of the checkpointable to save a pytree under.
      Defaults to 'pytree'.
    overwrite: If True, fully overwrites an existing checkpoint in `path`.
      Otherwise, raises an error if the checkpoint already exists.
    custom_metadata: User-provided custom metadata. An arbitrary
      JSON-serializable dictionary the user can use to store additional
      information. The field is treated as opaque by Orbax.

  Returns:
    An `AsyncResponse` that can be used to block until the save is complete.
    Blocking can be done using `response.result()`, which returns `None`.
  """
  validation.validate_state(state)
  return execution.save_checkpointables_impl(
      path,
      {checkpointable_name: state},
      overwrite=overwrite,
      custom_metadata=custom_metadata,
      async_origin=True,
  )

