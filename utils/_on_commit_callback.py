
def _on_commit_callback(
    tmpdir: atomicity_types.TemporaryPath,
    checkpoint_start_time: float,
):
  """Finalize atomic save and record checkpoint save metrics."""
  asyncio_utils.run_sync(
      atomicity.on_commit_callback(
          tmpdir,
          checkpoint_start_time=checkpoint_start_time,
      )
  )

