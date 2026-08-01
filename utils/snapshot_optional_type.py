
def snapshot_optional_type(typ: Type | None) -> SnapshotItem:
    if typ:
        return snapshot_type(typ)
    else:
        return ("<not set>",)

