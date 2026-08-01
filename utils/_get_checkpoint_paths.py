
def _get_checkpoint_paths(
  ckpt_dir: str | os.PathLike,
  step: int | float,
  prefix: str = 'checkpoint_',
) -> tuple[str, str, str]:
  """Generate the checkpoint paths used in this save operation."""
  ckpt_dir = os.fspath(ckpt_dir)  # Pathlib -> str
  logging.info('Saving checkpoint at step: %s', step)
  # normalize path because io.glob() can modify path './', '//' ...
  ckpt_dir = safe_normpath(ckpt_dir)
  ckpt_tmp_path = _checkpoint_path(ckpt_dir, 'tmp', prefix)
  ckpt_path = _checkpoint_path(ckpt_dir, step, prefix)
  base_path = os.path.join(ckpt_dir, prefix)
  return ckpt_path, ckpt_tmp_path, base_path

