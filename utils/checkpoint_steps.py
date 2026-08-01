
def checkpoint_steps(checkpoint_dir: epath.PathLike) -> List[int]:
  """Returns a list of finalized checkpoint steps in the directory."""
  return [
      step_from_checkpoint_name(s.name)
      for s in checkpoint_steps_paths(checkpoint_dir)
  ]

