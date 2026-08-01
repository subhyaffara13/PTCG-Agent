
def snapshot_types(types: Sequence[Type]) -> SnapshotItem:
    return tuple(snapshot_type(item) for item in types)

