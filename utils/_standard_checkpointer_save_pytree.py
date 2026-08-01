
def _standard_checkpointer_save_pytree(path: epath.Path) -> None:
  """Saves a direct checkpoint using StandardCheckpointer for pytree."""
  pytree = create_pytree()
  if _OVERWRITE.value:
    path.rmtree(missing_ok=True)
  with standard_checkpointer.StandardCheckpointer() as checkpointer:
    checkpointer.save(path, pytree, custom_metadata={'custom': 'meta'})

