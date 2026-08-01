
def impl_CONTAINS_OP_fallback(a: T, b: Iterable[T]) -> bool:
    # performs fallback "a in b"
    if hasattr(b, "__iter__"):
        # use __iter__ if __contains__ is not available
        for x in b:
            if x == a:
                return True
        return False
    raise TypeError(f"argument of type {type(b)} is not iterable")

