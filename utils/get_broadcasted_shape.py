
def get_broadcasted_shape(a: BlockShapeType, b: BlockShapeType) -> BlockShapeType:
    assert isinstance(a, Sequence)
    assert isinstance(b, Sequence)
    if len(a) > len(b):
        return get_broadcasted_shape(a, (*[1] * (len(a) - len(b)), *b))
    elif len(a) < len(b):
        b, a = a, b
        return get_broadcasted_shape(a, (*[1] * (len(a) - len(b)), *b))
    else:

        def _get_broadcasted_dim(d1: int | str, d2: int | str) -> int | str:
            if str(d1) == "1":
                return d2
            elif str(d2) == "1":
                return d1
            assert str(d1) == str(d2)
            return d1

        return tuple(_get_broadcasted_dim(d1, d2) for d1, d2 in zip(a, b))

