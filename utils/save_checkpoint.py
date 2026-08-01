
def save_checkpoint(
  ckpt_dir: str | os.PathLike,
  target: PyTree,
  step: int | float,
  prefix: str = 'checkpoint_',
  keep: int = 1,
  overwrite: bool = False,
  keep_every_n_steps: int | None = None,
  async_manager: AsyncManager | None = None,
  orbax_checkpointer: ocp.Checkpointer | None = None,
) -> str:
  """Save a checkpoint of the model. Suitable for single-host.

  In this method, every JAX process saves the checkpoint on its own. Do not
  use it if you have multiple processes and you intend for them to save data
  to a common directory (e.g., a GCloud bucket). To save multi-process
  checkpoints to a shared storage or to save ``GlobalDeviceArray``s, use
  ``save_checkpoint_multiprocess()`` instead.

  Pre-emption safe by writing to temporary before a final rename and cleanup
  of past files. However, if async_manager is used, the final
  commit will happen inside an async callback, which can be explicitly waited
  by calling ``async_manager.wait_previous_save()``.

  Example usage::

    >>> from flax.training import checkpoints
    >>> import jax.numpy as jnp
    >>> import tempfile

    >>> with tempfile.TemporaryDirectory() as dir_path:
    ...   test_object = {
    ...     'a': jnp.array([1, 2, 3], jnp.int32),
    ...     'b': jnp.array([1, 1, 1], jnp.int32),
    ...   }
    ...   file_path = checkpoints.save_checkpoint(
    ...     dir_path, target=test_object, step=0, prefix='test_', keep=1
    ...   )
    ...   restored_object = checkpoints.restore_checkpoint(
    ...     file_path, target=None
    ...   )
    >>> restored_object
    {'a': Array([1, 2, 3], dtype=int32), 'b': Array([1, 1, 1], dtype=int32)}

  Args:
    ckpt_dir: str or pathlib-like path to store checkpoint files in.
    target: serializable flax object, usually a flax optimizer.
    step: int or float: training step number or other metric number.
    prefix: str: checkpoint file name prefix.
    keep: number of past checkpoint files to keep.
    overwrite: overwrite existing checkpoint files if a checkpoint at the
      current or a later step already exits (default: False).
    keep_every_n_steps: if defined, keep every checkpoints every n steps (in
      addition to keeping the last 'keep' checkpoints).
    async_manager: if defined, the save will run without blocking the main
      thread. Only works for single host. Note that an ongoing save will still
      block subsequent saves, to make sure overwrite/keep logic works correctly.
    orbax_checkpointer: if defined, the save will be done by ocp. In the future,
      all Flax checkpointing features will be migrated to Orbax, and starting to
      use an ``orbax_checkpointer`` is recommended. Please check out the
      checkpointing guide
      (https://flax.readthedocs.io/en/latest/guides/training_techniques/use_checkpointing.html#save-checkpoints)
      for how to use Orbax checkpointers.

  Returns:
    Filename of saved checkpoint.
  """
  jax.monitoring.record_event('/jax/flax/checkpoint/save')
  start_time = time.time()
  # Make sure all saves are finished before the logic of checking and removing
  # outdated checkpoints happens.
  if async_manager:
    async_manager.wait_previous_save()

  ckpt_path, ckpt_tmp_path, base_path = _get_checkpoint_paths(
    ckpt_dir, step, prefix
  )

  if config.flax_use_orbax_checkpointing or orbax_checkpointer:
    logging.info(
      'Using Orbax as backend to save Flax checkpoints. For potential'
      ' troubleshooting see:'
      ' https://flax.readthedocs.io/en/latest/guides/training_techniques/use_checkpointing.html#orbax-as-backend-troubleshooting'
    )
    if jax.process_count() > 1:
      logging.warning(
        'Multiple JAX processes detected when calling single-process'
        ' `save_checkpoint`. Your devices will HANG if this function is only'
        ' called on process 0! Troubleshoot at:'
        ' https://flax.readthedocs.io/en/latest/guides/training_techniques/use_checkpointing.html#if-your-devices-hang-when-writing-checkpoints'
      )

    # Make sure any previous work is done before making file changes.
    if orbax_checkpointer and isinstance(
      orbax_checkpointer, ocp.AsyncCheckpointer
    ):
      orbax_checkpointer.wait_until_finished()
    # If no checkpointer provided, save synchronously with default setting.
    if not orbax_checkpointer:
      orbax_checkpointer = ocp.Checkpointer(
        ocp.PyTreeCheckpointHandler()
      )
    # Check singular target.
    if jtu.treedef_is_leaf(jtu.tree_structure(target)) and not isinstance(
      orbax_checkpointer._handler,
      ocp.ArrayCheckpointHandler,  # pylint: disable=protected-access
    ):
      raise ValueError(
        'Orbax backend only accept pytree as save target. To save singular'
        ' objects like numbers or Numpy arrays, checkout'
        ' https://flax.readthedocs.io/en/latest/guides/training_techniques/use_checkpointing.html#if-you-don-t-save-pytrees'
      )

    orbax_checkpointer.save(
      ckpt_path, target, force=overwrite
    )
    # Do a process check here in case people call this for multihost.
    if process_index() == 0:
      _remove_invalid_ckpts(
        ckpt_path, base_path, keep, overwrite, keep_every_n_steps, True
      )
    end_time = time.time()
    monitoring.record_event_duration_secs(
      _WRITE_CHECKPOINT_EVENT, end_time - start_time
    )
    return ckpt_path

  warnings.warn(
    (
      'Flax Checkpointing will soon be deprecated in favor of Orbax'
      ' (https://github.com/google/orbax). Please refer to the Checkpoint'
      ' Upgrade Guide'
      ' (https://flax.readthedocs.io/en/latest/guides/converting_and_upgrading/orbax_upgrade_guide.html)'
      ' to self-migrate your code to ocp.'
    ),
    DeprecationWarning,
  )
  if not overwrite:
    _check_overwrite_error(ckpt_tmp_path, ckpt_path, base_path, step)  # type: ignore

  target = serialization.to_bytes(target)

  # Save the files via I/O sync or async.
  def save_main_ckpt_task():
    jax.monitoring.record_event('/jax/flax/checkpoint/save_main_ckpt_task')
    return _save_main_ckpt_file(
      target,
      False,
      (ckpt_tmp_path, ckpt_path),
      base_path,
      step,
      keep,
      overwrite,
      keep_every_n_steps,
      start_time,
    )

  if async_manager:
    async_manager.save_async(save_main_ckpt_task)
  else:
    save_main_ckpt_task()
  end_time = time.time()
  monitoring.record_event_duration_secs(
    _WRITE_CHECKPOINT_EVENT, end_time - start_time
  )
  return ckpt_path

