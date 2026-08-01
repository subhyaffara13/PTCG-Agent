
def _checkpoint_path(
  ckpt_dir: str, step: int | float | str, prefix: str = 'checkpoint_'
) -> str:
  return os.path.join(ckpt_dir, f'{prefix}{step}')

