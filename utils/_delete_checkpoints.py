
def _delete_checkpoints(
    manager: p2p_checkpoint_manager.CheckpointManager,
    step: int,
    local_directory: epath.Path,
    delete_before_restore: str = 'local_p0',
):
  """Deletes checkpoints from the CheckpointManager."""
  step_dir = local_directory / str(step)
  if delete_before_restore == 'local_p0':
    if multihost.process_index() == 0 and step_dir.exists():
      logging.info(
          'Process 0: removing local checkpoint to trigger P2P restore.'
      )
      step_dir.rmtree()
      manager.reload()
  elif delete_before_restore == 'local_all':
    if step_dir.exists():
      logging.info(
          'All processes: removing local checkpoint to trigger GCS restore.'
      )
      step_dir.rmtree()
      manager.reload()
  elif delete_before_restore == 'none':
    logging.info('Skipping deletion of local checkpoint for local restore.')
  else:
    raise ValueError(
        f'Invalid delete_before_restore: {delete_before_restore}'
    )

