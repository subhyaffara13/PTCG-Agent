
def create_instance(
    source: epath.Path,
    snapshot: epath.Path,
    *,
    set_immutable: bool | None = None,
    snapshot_type: SnapshotType = SnapshotType.IN_PLACE,
):
  """Creates a snapshot instance according to the provided options."""
  if snapshot_type == SnapshotType.EMPTY:
    return _EmptySnapshot(source, snapshot)

  return _DefaultSnapshot(source, snapshot)

