
def checkpoint_steps_paths(
    checkpoint_dir: epath.PathLike,
) -> List[epath.Path]:
  """Returns a list of finalized checkpoint paths in the directory."""
  checkpoint_dir = epath.Path(checkpoint_dir)
  if not checkpoint_dir.exists():
    return []

  with futures.ThreadPoolExecutor() as executor:
    fs = {
        step_dir: executor.submit(
            _is_legacy_finalized_step_checkpoint, step_dir
        )
        for step_dir in checkpoint_dir.iterdir()
    }
    return [step_dir for step_dir, future in fs.items() if future.result()]

