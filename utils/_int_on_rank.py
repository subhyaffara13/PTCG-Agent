
def _int_on_rank(i: "int | LocalIntNode | ConstantIntNode", r: int) -> int:
    if isinstance(i, LocalIntNode):
        return i._local_ints[r]
    elif isinstance(i, ConstantIntNode):
        return i.val
    elif isinstance(i, int):
        return i
    else:
        raise AssertionError(type(i))

