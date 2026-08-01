
def sample_inputs_histc(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    sizes = ((), (S,), (S, S), (S, S, S), (S, 1, S), (S, 0, S))

    for size, min, max in product(sizes, [0, -10], [0, 10]):
        # construct sample input omitting bins arg
        yield SampleInput(make_arg(size), min=min, max=max)

        # construct sample inputs with a few different bins values
        for bins in [1, 3, 10]:
            yield SampleInput(make_arg(size), bins=bins, min=min, max=max)

