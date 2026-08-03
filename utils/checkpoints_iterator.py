import logging
import time
from typing import Callable, Optional

def checkpoints_iterator(
    checkpoint_dir: epath.PathLike,
    *,
    min_interval_secs: int = 0,
    seconds_to_sleep: int = 1,
    timeout: Optional[int] = None,
    timeout_fn: Optional[Callable[[], bool]] = None,
    step_prefix: Optional[str] = None,
    step_format_fixed_length: Optional[int] = None,
    step_name_format: Optional[step_lib.NameFormat[step_lib.Metadata]] = None,
    snapshot_dir: Optional[epath.Path] = None,
    set_immutable: bool | None = None,
    ignore_snapshot_errors: bool | None = True,
) -> Iterator[int]:
  """Continuously yield new checkpoint files as they appear.

  Based on the equivalent TF method.

  The iterator only checks for new checkpoints when control flow has been
  reverted to it. This means it can miss checkpoints if your code takes longer
  to run between iterations than `min_interval_secs` or the interval at which
  new checkpoints are written.

  Warning: If CheckpointManager is running in a different process for training
  and is cleaning up old checkpoints (via the `max_to_keep` argument), steps
  returned by this function may not be valid after being clean up by another
  process. In this case, `max_to_keep` should be increased (suggested value: 5)

  The `timeout` argument is the maximum number of seconds to block waiting for
  a new checkpoint.  It is used in combination with the `timeout_fn` as
  follows:

  * If the timeout expires and no `timeout_fn` was specified, the iterator
    stops yielding.
  * If a `timeout_fn` was specified, that function is called and if it returns
    a true boolean value the iterator stops yielding.
  * If the function returns a false boolean value then the iterator resumes the
    wait for new checkpoints.  At this point the timeout logic applies again.

  This behavior gives control to callers on what to do if checkpoints do not
  come fast enough or stop being generated.  For example, if callers have a way
  to detect that the training has stopped and know that no new checkpoints
  will be generated, they can provide a `timeout_fn` that returns `True` when
  the training has stopped.  If they know that the training is still going on
  they return `False` instead.

  Args:
    checkpoint_dir: The directory in which checkpoints are saved.
    min_interval_secs: The minimum number of seconds between yielding
      checkpoints.
    seconds_to_sleep: Seconds to sleep if a checkpoint is not found. Note the
      difference with min_interval_secs, which puts a lower bound on how when a
      new checkpoint will be looked for after yielding one checkpoint.
      seconds_to_sleep instead specifies how we should sleep for if no new
      checkpoints are found. Note that the timeout is only checked when not
      sleeping, so a `seconds_to_sleep` longer than the timeout would result in
      timing out after `seconds_to_sleep` seconds rather than `timeout` seconds.
    timeout: The maximum number of seconds to wait between checkpoints. The
      function will time out if `timeout` seconds have passed since a new
      checkpoint step was found. If left as `None`, then the process will wait
      indefinitely.
    timeout_fn: Optional function called after a timeout. If the function
      returns True, then it means that no new checkpoints will be generated and
      the iterator will exit. The function is called with no arguments.
    step_prefix: A prefix applied to step numbers (e.g. <prefix>_42).
    step_format_fixed_length: Expects to find checkpoint step directories with
      exactly this number of digits (leading zeros if necessary).
    step_name_format: Step NameFormat used to find step under given root
      directory. If provided, `step_prefix` and `step_format_fixed_length` are
      ignored.
    snapshot_dir: The directory in which snapshots are saved. If not provided,
      the snapshot directory is created as `checkpoint_dir / _SNAPSHOTS`.
    set_immutable: If True and applicable, sets the files in the snapshot to be
      immutable.
    ignore_snapshot_errors: If True, ignore errors when creating/releasing
      snapshots.

  Yields:
    Integer step numbers of the latest checkpoints as they arrive.
  """
  checkpoint_dir = epath.Path(checkpoint_dir)
  step_name_format = _init_step_name_format(
      step_name_format=step_name_format,
      step_prefix=step_prefix,
      step_format_fixed_length=step_format_fixed_length,
  )
  if snapshot_dir is None:
    snapshot_dir = checkpoint_dir / _SNAPSHOTS
  if snapshot_dir.exists():
    for step_dir in snapshot_dir.iterdir():
      snapshot_impl = snapshot_lib.create_instance(checkpoint_dir, step_dir)
      with _manage_snapshot_file_not_found(
          ignore_errors=ignore_snapshot_errors,
          formatted_message=(
              'Ignoring error when cleaning up leftover snapshot:'
              f' {step_dir.name}'
          ),
      ):
        asyncio_utils.run_sync(snapshot_impl.release_snapshot())
  checkpoint_step = None
  while True:
    until_step = checkpoint_step + 1 if checkpoint_step is not None else None
    with wait_for_new_checkpoint(
        checkpoint_dir,
        until_step=until_step,
        seconds_to_sleep=seconds_to_sleep,
        timeout=timeout,
        timeout_fn=timeout_fn,
        step_name_format=step_name_format,
        snapshot_dir=snapshot_dir,
        set_immutable=set_immutable,
        ignore_snapshot_errors=ignore_snapshot_errors,
    ) as new_checkpoint_step:
      if new_checkpoint_step == -1:
        if not timeout_fn:
          logging.info('Timed-out waiting for a checkpoint.')
          return
        if timeout_fn():
          # The timeout_fn indicated that we are truly done.
          return
        else:
          # The timeout_fn indicated that more checkpoints may come.
          continue
      start = time.time()
      checkpoint_step = new_checkpoint_step
      yield checkpoint_step
    time_to_next_eval = start + min_interval_secs - time.time()
    if time_to_next_eval > 0:
      time.sleep(time_to_next_eval)

