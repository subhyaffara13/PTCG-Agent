
def create_contiguous(shape: Sequence[Int]) -> list[Int]:
    strides: list[Int] = [1]
    for dim in reversed(shape[:-1]):
        strides.append(dim * strides[-1])  # type: ignore[operator]
    return list(reversed(strides))

