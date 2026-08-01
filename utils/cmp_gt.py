
def cmp_gt(a: Any, b: Any) -> bool:
    # Check if __gt__ is overridden
    if isinstance(type(a).__gt__, types.FunctionType):
        return a.__gt__(b)
    # a > b is equivalent to b < a
    return cmp_lt(b, a)

