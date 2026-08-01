
def sample_inputs_take_along_dim(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad, low=None, high=None)
    yield SampleInput(
        make_arg((S, S)), gather_variable((S, S), 1, S, True, device=device), 0)

    # `indices` broadcast
    yield SampleInput(
        make_arg((S, S)), gather_variable((1, S // 2), 0, S, True, device=device), 1)

    # `self` broadcast
    yield SampleInput(
        make_arg((1, S)), gather_variable((S, S // 2), 0, S, True, device=device), 1)

    # without `dim` arg
    yield SampleInput(
        make_arg((S, S)), gather_variable((S, S // 2), 0, S, True, device=device))

    # Negative indices sample — guarded against python_ref
    if not kwargs.get('is_python_ref', False):
        neg_idx = gather_variable((S, S), 1, S, True, device=device) - S
        yield SampleInput(
            make_arg((S, S)),
            neg_idx,
            1)

