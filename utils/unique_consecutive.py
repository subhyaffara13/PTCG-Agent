
def unique_consecutive(
    fake_mode: FakeTensorMode,
    func: OpOverload,
    arg: FakeTensor,
    return_inverse: bool = False,
    return_counts: bool = False,
    dim: int | None = None,
) -> tuple[FakeTensor, FakeTensor, FakeTensor]:
    return _unique(
        fake_mode,
        func,
        arg,
        dim,
        False,
        return_inverse,
        return_counts,
        unique_consecutive=True,
    )

