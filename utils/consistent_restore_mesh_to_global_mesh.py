
def consistent_restore_mesh_to_global_mesh(
    state: PyTree,
    shardings: PyTree,
) -> PyTree:
  """Transfers from consistent restore mesh to global mesh."""
  logging.info('Transferring from consistent restore mesh to global mesh')

  start_transfer = time.time()
  resharded_state = jax.device_put(state, shardings, donate=True)
  transfer_elapsed_s = time.time() - start_transfer
  logging.info(
      'Finished transferring from consistent restore mesh to global mesh'
      ' in %.2fs',
      transfer_elapsed_s,
  )
  jax.monitoring.record_event_duration_secs(
      '/orbax/emergency/checkpoint/read/transfer_global_shard_duration_secs',
      transfer_elapsed_s,
  )

  return resharded_state

