
def delete_checkpoint_metadata_field(
    path: epath.Path, field_to_remove: str
) -> None:
  """Deletes a field from _CHECKPOINT_METADATA."""
  metadata_path = path / '_CHECKPOINT_METADATA'
  with open(metadata_path, 'r') as f:
    data = json.load(f)
  del data[field_to_remove]
  with open(metadata_path, 'w') as f:
    json.dump(data, f)


def delete_checkpoint_metadata_field(
    path: epath.Path, field_to_remove: str
) -> None:
  """Deletes a field from _CHECKPOINT_METADATA."""
  metadata_path = path / '_CHECKPOINT_METADATA'
  with open(metadata_path, 'r') as f:
    data = json.load(f)
  del data[field_to_remove]
  with open(metadata_path, 'w') as f:
    json.dump(data, f)

