
def tuple_max(a: IntTuple) -> int:
    if is_tuple(a):
        return max(tuple_max(x) for x in a)
    else:
        return a

