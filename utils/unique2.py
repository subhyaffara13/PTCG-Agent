
def unique2(
    fake_mode: FakeTensorMode,
    func: OpOverload,
    arg: FakeTensor,
    sorted: bool = True,
    return_inverse: bool = False,
    return_counts: bool = False,
) -> tuple[FakeTensor, FakeTensor, FakeTensor]:
    return _unique(fake_mode, func, arg, None, sorted, return_inverse, return_counts)

