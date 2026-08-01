
def v1_delete_checkpointable() -> None:
  """Saves a checkpointables checkpoint and deletes a checkpointable."""
  # Note: this is a non-critical alteration because each checkpointable is
  # separable and we allow deleting specific checkpointables as needed.
  # Restoring the checkpoint does not raise an error, as long as we don't
  # attempt to restore the deleted checkpointable.
  path = (
      epath.Path(_BASE_DIR.value)
      / 'v1_checkpoints'
      / 'composite_checkpoint'
      / 'non_critical_general_alterations'
      / 'deleted_checkpointable'
  )
  generate_v1_checkpoint(path)
  (path / 'state').rmtree()

