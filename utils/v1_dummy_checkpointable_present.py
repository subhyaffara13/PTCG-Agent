
def v1_dummy_checkpointable_present() -> None:
  """Saves a checkpointables checkpoint and adds a dummy checkpointable."""
  # Note: this is a critical alteration because a checkpointable is added to
  # the checkpoint and causes error when calling load_checkpointables with
  # `abstract_checkpointables=None`, which attempts to load all contents of the
  # checkpoint and will fail to restore the contents of a dummmy checkpointable.
  path = (
      epath.Path(_BASE_DIR.value)
      / 'v1_checkpoints'
      / 'composite_checkpoint'
      / 'critical_general_alterations'
      / 'dummy_checkpointable_added'
  )
  generate_v1_checkpoint(path)
  (path / 'dummy').mkdir()
  (path / 'dummy' / '_METADATA').write_text('dummy')

