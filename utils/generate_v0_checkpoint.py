
def generate_v0_checkpoint(
    path: epath.Path,
    is_direct_checkpoint: bool = False,
) -> None:
  """Generates a V0 checkpoint with the given save function."""
  if is_direct_checkpoint:
    _standard_checkpointer_save_pytree(path)
    (path / 'descriptor').rmtree()  # GOOGLE_INTERNAL
  else:
    _checkpointer_save_composite_mixed(path)
    (path / 'state' / 'descriptor').rmtree()  # GOOGLE_INTERNAL

