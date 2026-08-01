
def _length(obj) -> int:
    if obj is None:
        return 0
    if not isinstance(obj, Sequence):
        return 1
    return len(obj)

