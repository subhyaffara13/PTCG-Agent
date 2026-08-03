import logging
from typing import Callable, Optional

def wait_for_new_checkpoint(
    checkpoint_dir: epath.Path,
    *,
    until_step: Optional[int] = None,
    seconds_to_sleep: int = 1,
    timeout: Optional[int] = None,
    timeout_fn: Optional[Callable[[], bool]] = None,
    step_prefix: Optional[str] = None,
    step_format_fixed_length: Optional[int] = None,
    step_name_format: Optional[step_lib.NameFormat[step_lib.Metadata]] = None,
    snapshot_dir: Optional[epath.Path] = None,
    set_immutable: bool | None = None,
    ignore_snapshot_errors: bool | None = True,
):
  """Waits until a new checkpoint file is found.

  Automatically snapshots any checkpoint that is returned, and releases the
  snapshot of the checkpoint when execution returns to this function.

  Args:
    checkpoint_dir: The directory in which checkpoints are saved.
    until_step: If specified, waits until a step greater than or equal to
      `until_step` has been found. If set to None (default), returns the first
      step found.
    seconds_to_sleep: The number of seconds to sleep for before looking for a
      new checkpoint.
    timeout: The maximum number of seconds to wait. If left as `None`, then the
      process will wait indefinitely.
    timeout_fn: Optional function to call after a timeout.  If the function
      returns True, then it means that no new checkpoints will be generated and
      the iterator will exit.  The function is called with no arguments.
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
    a new checkpoint step, or -1 if the timeout was reached.
  """
  step_name_format = _init_step_name_format(
      step_name_format=step_name_format,
      step_prefix=step_prefix,
      step_format_fixed_length=step_format_fixed_length,
  )
  step = _wait_for_new_checkpoint(
      checkpoint_dir,
      step_name_format=step_name_format,
      until_step=until_step,
      seconds_to_sleep=seconds_to_sleep,
      timeout=timeout,
      timeout_fn=timeout_fn,
      snapshot_dir=snapshot_dir,
      set_immutable=set_immutable,
      ignore_snapshot_errors=ignore_snapshot_errors,
  )
  try:
    yield step
  finally:
    # Release snapshot on the checkpoint step.
    if step != -1:
      logging.info(
          'Releasing snapshot for step: %d after releasing control.', step
      )
      _release_snapshot(
          checkpoint_dir,
          step,
          step_name_format,
          snapshot_dir,
          ignore_file_not_found_error=ignore_snapshot_errors,
      )

