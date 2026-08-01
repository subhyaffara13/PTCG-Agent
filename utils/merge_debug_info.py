
def merge_debug_info(
    lhs: tuple[str, ...] | None,
    rhs: tuple[str, ...] | None,
) -> tuple[str, ...] | None:
    # Ensure that when merging, each entry shows up just once.
    if lhs is None and rhs is None:
        return None

    return tuple(set((lhs or ()) + (rhs or ())))

