
def snapshot_type(typ: Type) -> SnapshotItem:
    """Create a snapshot representation of a type using nested tuples."""
    return typ.accept(SnapshotTypeVisitor())

