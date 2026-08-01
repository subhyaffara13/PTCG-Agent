
def save_checkpointables_async(
    path: path_types.PathLike,
    checkpointables: dict[str, Checkpointable],
    *,
    overwrite: bool = False,
    custom_metadata: tree_types.JsonType | None = None,
) -> async_types.AsyncResponse[None]:
  """Saves a dictionary of checkpointables asynchronously.

  See :py:func:`.save_checkpointables`
  documentation.

  Unlike :py:func:`.save_checkpointables`, this function returns immediately
  after the save operation is scheduled
  (except for certain operations, like device-to-host copying of on-device
  arrays, which must happen on the main thread). Further writing operations
  continue in a background thread. An :py:class:`~.AsyncResponse` is returned
  that can be used to block until the save is complete (using
  `response.result()`). Make sure to wait for completion before attempting to
  load the checkpoint or exiting the program. This function should be called on
  all available controller processes.

  Example usage:
    Saving multiple distinct components (e.g. model parameters and dataset
    iterator) asynchronously::
      path = '/tmp/my_checkpoint_step_100'

      # Setup components
      params = {'w': jnp.ones((8, 8)), 'b': jnp.zeros(8)}

      # Setup Grain iterator (Stateful Checkpointable)
      import grain
      dataset_iter = iter(
          grain.MapDataset.range(30)
          .batch(3)
          .map(lambda x: x.tolist())
      )

      # Save multiple components
      checkpointables = {
          'model': params,
          'dataset': dataset_iter,
      }

      # Start the async save
      response = ocp.save_checkpointables_async(path, checkpointables)

      # Perform other operations here...

      # Wait for the save to finish
      response.result()

  Args:
    path: The path to save the checkpoint to.
    checkpointables: A dictionary of checkpointables. Dictionary keys represent
      the names of the checkpointables, while the values are the checkpointable
      objects themselves.
    overwrite: If True, fully overwrites an existing checkpoint in `path`.
      Otherwise, raises an error if the checkpoint already exists.
    custom_metadata: User-provided custom metadata. An arbitrary
      JSON-serializable dictionary the user can use to store additional
      information. The field is treated as opaque by Orbax.

  Returns:
    An `AsyncResponse` that can be used to block until the save is complete.
    Blocking can be done using `response.result()`, which returns `None`.
  """
  validation.validate_save_checkpointables(checkpointables)
  return execution.save_checkpointables_impl(
      path,
      checkpointables,
      overwrite=overwrite,
      custom_metadata=custom_metadata,
      async_origin=True,
  )

