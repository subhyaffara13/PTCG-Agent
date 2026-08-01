
def _wait_for_new_checkpoint(
    checkpoint_dir: epath.Path,
    *,
    step_name_format: step_lib.NameFormat[step_lib.Metadata],
    until_step: Optional[int] = None,
    seconds_to_sleep: int = 1,
    timeout: Optional[int] = None,
    timeout_fn: Optional[Callable[[], bool]] = None,
    snapshot_dir: Optional[epath.Path] = None,
    set_immutable: bool | None = None,
    ignore_snapshot_errors: bool | None = None,
) -> int:
  """See documentation for wait_for_new_checkpoint."""
  start = time.time()
  stop_time = start + timeout if timeout is not None else None

  def _sleep_and_maybe_exit():
    if stop_time is not None and time.time() + seconds_to_sleep > stop_time:
      if timeout_fn is None:
        return True
      elif timeout_fn():  # Only exit when timeout_fn indicates completion.
        return True
    logging.info('Sleeping for %d seconds.', seconds_to_sleep)
    time.sleep(seconds_to_sleep)
    return False

  log_str = f'Waiting for new checkpoint at {checkpoint_dir}. '
  if until_step is not None:
    log_str += f'Waiting until step {until_step} is reached. '
  if timeout is not None:
    log_str += f'Will time out after {timeout} seconds. '
  logging.info(log_str)

  result = -1
  if multihost.process_index() == 0:
    while True:
      if not checkpoint_dir.exists():
        if _sleep_and_maybe_exit():
          break
        continue  # continue waiting until directory creation or timeout.

      steps = utils.checkpoint_steps(checkpoint_dir)
      checkpoint_step = max(steps) if steps else None
      if _reached_desired_step(checkpoint_step, until_step):
        if not _snapshot_checkpoint(
            checkpoint_dir,
            checkpoint_step,
            step_name_format,
            snapshot_dir,
            set_immutable=set_immutable,
            ignore_file_not_found_error=ignore_snapshot_errors,
        ):
          continue
        result = checkpoint_step
        break
      elif _sleep_and_maybe_exit():
        break

  result = multihost.broadcast_one_to_all(np.int32(result)).item()
  wait_duration = time.time() - start
  jax.monitoring.record_event_duration_secs(
      '/jax/orbax/checkpoint_utils/wait_duration', wait_duration
  )

  if result == -1:
    logging.info('Timed out waiting for new checkpoint. Returning -1.')
  else:
    logging.info('Found new checkpoint step: %d.', result)
  return result

