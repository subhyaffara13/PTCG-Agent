
def restore_checkpoint(
  ckpt_dir: str | os.PathLike,
  target: Any | None,
  step: int | float | None = None,
  prefix: str = 'checkpoint_',
  parallel: bool = True,
  gda_manager: GlobalAsyncCheckpointManager | None = None,
  allow_partial_mpa_restoration: bool = False,
  orbax_checkpointer: ocp.Checkpointer | None = None,
  orbax_transforms: dict | None = None,
) -> PyTree:
  """Restore last/best checkpoint from checkpoints in path.

  Sorts the checkpoint files naturally, returning the highest-valued
  file, e.g.:

  *  ``ckpt_1, ckpt_2, ckpt_3 --> ckpt_3``

  *  ``ckpt_0.01, ckpt_0.1, ckpt_0.001 --> ckpt_0.1``

  *  ``ckpt_-1.0, ckpt_1.0, ckpt_1e5 --> ckpt_1e5``

  Example usage::

    >>> from flax.training import checkpoints
    >>> import jax.numpy as jnp
    >>> import tempfile
    ...
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
    ckpt_dir: str: checkpoint file or directory of checkpoints to restore from.
    target: matching object to rebuild via deserialized state-dict. If None, the
      deserialized state-dict is returned as-is.
    step: int or float: step number to load or None to load latest. If
      specified, ckpt_dir must be a directory.
    prefix: str: name prefix of checkpoint files.
    parallel: bool: whether to load seekable checkpoints in parallel, for speed.
    gda_manager: required if checkpoint contains a multiprocess array
      (GlobalDeviceArray or jax Array from pjit). Will read the arrays from the
      separate subdirectory with postfix "_gda".
    allow_partial_mpa_restoration: If true, the given ``target`` doesn't have to
      contain all valid multiprocess arrays. As a result, the restored Pytree
      may have some MPAs not restored correctly. Use this if you cannot provide
      a fully valid ``target`` and don't need all the MPAs in the checkpoint to
      be restored.
    orbax_checkpointer: the ``ocp.Checkpointer`` that handles the underlying
      restore, if the given checkpoint is saved with ocp.
    orbax_transforms: the Orbax transformations that will be passed into
      ``orbax_checkpointer.restore()`` call.

  Returns:
    Restored ``target`` updated from checkpoint file, or if no step specified
    and
    no checkpoint files present, returns the passed-in ``target`` unchanged.
    If a file path is specified and is not found, the passed-in ``target`` will
    be
    returned. This is to match the behavior of the case where a directory path
    is specified but the directory has not yet been created.
  """
  jax.monitoring.record_event('/jax/flax/checkpoint/restore')
  start_time = time.time()
  # Make sure any previous work is done before checking files.
  if orbax_checkpointer and isinstance(
    orbax_checkpointer, ocp.AsyncCheckpointer
  ):
    orbax_checkpointer.wait_until_finished()

  ckpt_dir = os.fspath(ckpt_dir)  # Pathlib -> str
  ckpt_dir = safe_normpath(ckpt_dir)
  if step is not None:
    ckpt_path = _checkpoint_path(ckpt_dir, step, prefix)
    if not io.exists(ckpt_path):
      raise ValueError(f'Matching checkpoint not found: {ckpt_path}')
  else:
    if not io.exists(ckpt_dir):
      logging.info('Found no checkpoint directory at %s', ckpt_dir)
      return target
    if io.isdir(ckpt_dir):
      # This means the given dir is an orbax checkpoint.
      if _is_orbax_checkpoint(ckpt_dir):
        ckpt_path = ckpt_dir
      else:
        ckpt_path = latest_checkpoint(ckpt_dir, prefix)  # type: ignore
        if not ckpt_path:
          logging.info(
            'Found no checkpoint files in %s with prefix %s', ckpt_dir, prefix
          )
          return target
    else:
      ckpt_path = ckpt_dir

  # Restore the checkpoint with Orbax if needed.
  is_orbax = _is_orbax_checkpoint(ckpt_path)
  ckpt_type = 'orbax' if is_orbax else 'legacy Flax'
  logging.info(f'Restoring {ckpt_type} checkpoint from {ckpt_path}')
  if is_orbax:
    if not orbax_checkpointer:
      orbax_checkpointer = ocp.Checkpointer(
        ocp.PyTreeCheckpointHandler()
      )

    restore_kwargs = {}
    if target is not None:
      restore_kwargs['restore_args'] = orbax_utils.restore_args_from_target(
        target
      )
      if isinstance(orbax_checkpointer._handler, ocp.PyTreeCheckpointHandler):  # pylint: disable=protected-access
        restore_kwargs[
          'transforms'
        ] = orbax_utils.maybe_construct_transformations(
          target, orbax_transforms
        )
    restored = orbax_checkpointer.restore(
      ckpt_path, item=target, **restore_kwargs
    )
    restored = serialization.to_state_dict(restored)
    if target is not None:
      restored = serialization.from_state_dict(target, restored)
    end_time = time.time()
    monitoring.record_event_duration_secs(
      _READ_CHECKPOINT_EVENT, end_time - start_time
    )
    return restored

  # Legacy Flax checkpoint restoration.
  ckpt_size = io.getsize(ckpt_path)
  with io.GFile(ckpt_path, 'rb') as fp:
    if parallel and fp.seekable():
      buf_size = 128 << 20  # 128M buffer.
      num_bufs = ckpt_size / buf_size
      logging.debug('num_bufs: %d', num_bufs)
      checkpoint_contents = bytearray(ckpt_size)

      def read_chunk(i):
        # NOTE: We have to re-open the file to read each chunk, otherwise the
        # parallelism has no effect. But we could reuse the file pointers
        # within each thread.
        with io.GFile(ckpt_path, 'rb') as f:
          f.seek(i * buf_size)
          buf = f.read(buf_size)
          if buf:
            checkpoint_contents[i * buf_size : i * buf_size + len(buf)] = buf
          return len(buf) / buf_size

      pool_size = 32
      pool = thread.ThreadPoolExecutor(pool_size)
      results = pool.map(read_chunk, range(int(num_bufs) + 1))
      pool.shutdown(wait=False)
      logging.debug(f'results: {list(results)}')
    else:
      checkpoint_contents = fp.read()

  state_dict = serialization.msgpack_restore(checkpoint_contents)
  state_dict = _restore_mpas(
    state_dict,
    target,
    ckpt_path,
    step,
    gda_manager,
    allow_partial_mpa_restoration,
  )

  if target is None:
    restored_checkpoint = state_dict
  else:
    restored_checkpoint = serialization.from_state_dict(target, state_dict)

  end_time = time.time()
  monitoring.record_event_duration_secs(
    _READ_CHECKPOINT_EVENT, end_time - start_time
  )

  return restored_checkpoint

