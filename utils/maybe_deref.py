
def maybe_deref(
    weak_ref: StorageWeakRefWrapper | None,
) -> tuple[StorageWeakRefPointer, int] | None:
    if weak_ref is None:
        return None
    r = weak_ref()
    if r is None:
        return None
    # NB: r.data_ptr() does not necessarily equal weak_ref.data_ptr()
    return r, weak_ref.data_ptr()

