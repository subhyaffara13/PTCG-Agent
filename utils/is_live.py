
def is_live(weak_ref: StorageWeakRefWrapper | None) -> bool:
    return maybe_deref(weak_ref) is not None

