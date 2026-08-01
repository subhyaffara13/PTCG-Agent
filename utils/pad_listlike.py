
def pad_listlike(x: int | Sequence[int], size: int) -> Sequence[int]:
    if isinstance(x, int):
        return [x] * size
    if len(x) == 1:
        return type(x)([x[0]]) * size  # type: ignore[call-arg, operator, return-value]
    return x

