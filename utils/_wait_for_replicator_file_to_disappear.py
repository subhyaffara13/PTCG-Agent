
def _wait_for_replicator_file_to_disappear(
    local_checkpoint_directory: epath.Path, *, timeout_seconds: int = 300
):
  """Waits for the MTC daemonset to consume `replicator.yaml`."""
  replicator_file = epath.Path(local_checkpoint_directory) / _REPLICATOR_FILE
  logging.info(
      f'Waiting for {replicator_file} to disappear '
      f'(timeout={timeout_seconds}s)...'
  )
  for t in range(timeout_seconds):
    if not replicator_file.exists():
      logging.info('replicator.yaml no longer exists (waited %ds).', t)
      return
    time.sleep(1)
  raise TimeoutError(
      f'Timeout reached ({timeout_seconds} seconds) while waiting for'
      f' {_REPLICATOR_FILE} to disappear.'
  )

