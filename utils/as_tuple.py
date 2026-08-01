
def as_tuple(x: IntTuple) -> tuple[IntTuple, ...]:
    if is_int(x):
        return (x,)
    return x

