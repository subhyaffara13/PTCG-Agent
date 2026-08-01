
def is_full_slice(obj, line: int) -> bool:
    """
    We have a full length slice.
    """
    return (
        isinstance(obj, slice)
        and obj.start == 0
        and obj.stop == line
        and obj.step is None
    )

