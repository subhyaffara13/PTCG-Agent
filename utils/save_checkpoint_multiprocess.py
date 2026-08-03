import logging
import os
import time

def save_checkpoint_multiprocess(
  ckpt_dir: str | os.PathLike,
  target: PyTree,
  step: int | float,
  prefix: str = 'checkpoint_',
  keep: int = 1,
  overwrite: bool = False,
  keep_every_n_steps: int | None = None,
  async_manager: AsyncManager | None = None,
  gda_manager: GlobalAsyncCheckpointManager | None = None,
  orbax_checkpointer: ocp.Checkpointer | None = None,
) -> str:
  """Save a checkpoint of the model in multi-process environment.

  Use this method to save ``GlobalDeviceArray``s, or to save data to a
  common directory. Only process 0 will save the main checkpoint file and
  remove old checkpoint files.

  Pre-emption safe by writing to temporary before a final rename and cleanup
  of past files. However, if async_manager or gda_manager is used, the final
  commit will happen inside an async callback, which can be explicitly waited
  by calling ``async_manager.wait_previous_save()`` or
  ``gda_manager.wait_until_finished()``.

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
    gda_manager: required if target contains a JAX GlobalDeviceArray. Will save
      the GDAs to a separate subdirectory with postfix "_gda" asynchronously.
      Same as async_manager, this will block subsequent saves.
    orbax_checkpointer: if defined, the save will be done by Orbax. In the
      future, all Flax checkpointing features will be migrated to Orbax, and
      starting to use an ``orbax_checkpointer`` is recommended. Please check out
      the checkpointing guide
      (https://flax.readthedocs.io/en/latest/guides/training_techniques/use_checkpointing.html#save-checkpoints)
      for how to use Orbax checkpointers.

  Returns:
    Filename of saved checkpoint.
  """
  jax.monitoring.record_event('/jax/flax/checkpoint/save')
  start_time = time.time()
  # Make sure all saves are finished before the logic of checking and removing
  # outdated checkpoints happens.
  sync_global_devices('Flax:Checkpoint:StartSave')
  if async_manager:
    async_manager.wait_previous_save()
  if gda_manager:
    gda_manager.wait_until_finished()
    sync_global_devices('Flax:Checkpoint:WaitLastSaveDone')

  ckpt_path, ckpt_tmp_path, base_path = _get_checkpoint_paths(
    ckpt_dir, step, prefix
  )

  if config.flax_use_orbax_checkpointing or orbax_checkpointer:
    logging.info(
      'Using Orbax as backend to save Flax checkpoints. For potential'
      ' troubleshooting see:'
      ' https://flax.readthedocs.io/en/latest/guides/training_techniques/use_checkpointing.html#orbax-as-backend-troubleshooting'
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

    if process_index() == 0:
      _remove_invalid_ckpts(
        ckpt_path, base_path, keep, overwrite, keep_every_n_steps, True
      )
    orbax_checkpointer.save(
      ckpt_path, target, force=overwrite
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

  target = serialization.to_state_dict(target)
  target, mpa_targets = _split_mp_arrays(target)
  target = serialization.msgpack_serialize(target)
  has_mpa = bool(mpa_targets)

  if not overwrite:
    _check_overwrite_error(ckpt_tmp_path, ckpt_path, base_path, step)  # type: ignore
    sync_global_devices('Flax:Checkpoint:CheckOverwriteBeforeSave')

  # Save the files via I/O sync or async.
  def save_main_ckpt_task():
    jax.monitoring.record_event('/jax/flax/checkpoint/save_main_ckpt_task')
    return _save_main_ckpt_file(
      target,
      has_mpa,
      (ckpt_tmp_path, ckpt_path),
      base_path,
      step,
      keep,
      overwrite,
      keep_every_n_steps,
      start_time,
    )

  # Write the main checkpoint file only via process 0, to avoid race condition.
  if process_index() == 0:
    if async_manager:
      async_manager.save_async(save_main_ckpt_task)
    else:
      save_main_ckpt_task()

  if has_mpa:
    if not gda_manager:
      raise errors.MPACheckpointingRequiredError(ckpt_path, step)
    # Creating the directory containing GDAs explicitly. This should happen only
    # on process 0 and before any worker starts to write GDA data.
    if process_index() == 0:
      _make_mpa_dirs(mpa_targets, ckpt_tmp_path)
    sync_global_devices('Flax:Checkpoint:AfterCreateMPADir')
    _save_mpas(
      gda_manager,
      mpa_targets,
      ckpt_tmp_path,
      ckpt_path,
      base_path,
      keep,
      overwrite,
      keep_every_n_steps,
      start_time,
      async_manager,
    )

  end_time = time.time()
  monitoring.record_event_duration_secs(
    _WRITE_CHECKPOINT_EVENT, end_time - start_time
  )
  return ckpt_path

