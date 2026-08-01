
def sample_inputs_eye(op, device, dtype, requires_grad, **kwargs):
    # only ints >= 0 are allowed for both arguments, unless m is omitted
    sizes = (None, 0, 1, 2, 3, 4, 7, L, M, S)

    for n, m in product(sizes, sizes):
        if n is None:
            continue

        # TODO: no layout
        _kwargs = {'device': device, 'dtype': dtype, 'requires_grad': requires_grad}
        if m is None:
            yield SampleInput(n, args=(), kwargs=_kwargs)
        else:
            yield SampleInput(n, args=(m,), kwargs=_kwargs)

