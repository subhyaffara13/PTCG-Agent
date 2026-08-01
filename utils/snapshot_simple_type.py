
def snapshot_simple_type(typ: Type) -> SnapshotItem:
    return (type(typ).__name__,)

