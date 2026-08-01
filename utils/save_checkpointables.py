
def save_checkpointables(
    path: path_types.PathLike,
    checkpointables: dict[str, Checkpointable],
    *,
    overwrite: bool = False,
    custom_metadata: tree_types.JsonType | None = None,
) -> None:
  """Saves a dictionary of checkpointables.

  A “checkpointable” refers to a logical piece of the checkpoint that is
  distinct in some way from other pieces. Checkpointables are separable;
  they may or may not be loaded concurrently and some may be omitted from the
  checkpoint entirely. Checkpointables are often represented by different types,
  and have different representations on disk. The quintessential example is
  model params vs. dataset.

  For example, one might do::

    ocp.save_checkpointables(
        path,
        {
            'params': pytree_of_arrays,
            'dataset': pygrain.DatasetIterator(...),
        }
    )

  It is also possible to do::

    train_state = {
        'params': params_pytree_of_arrays,
        'opt_state': opt_state_pytree_of_arrays,
        'step': step,
        ...
    }
    ocp.save_checkpointables(path, train_state)

  This is not the ideal way of doing things because it is then difficult to run
  transformations that involve the entire train state (see the
  `load_and_transform` API).

  This function should be called on all available controller processes.

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
  """
  validation.validate_save_checkpointables(checkpointables)
  execution.save_checkpointables_impl(
      path,
      checkpointables,
      overwrite=overwrite,
      custom_metadata=custom_metadata,
      async_origin=False,
  ).result()

