import itertools

def sample_inputs_pdist(op_info, device, dtype, requires_grad, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    yield from (SampleInput(make_input((n, m))) for n, m in itertools.product((1, S), repeat=2))
    yield from (SampleInput(make_input((S, S)), kwargs=dict(p=p)) for p in (0.0, 1.0, 2.0, 10.0, float("inf")))

