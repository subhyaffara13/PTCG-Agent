
def sample_inputs_cross(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(
        make_tensor, dtype=dtype, device=device, requires_grad=requires_grad
    )
    yield SampleInput(make_arg((S, 3)), args=(make_arg((S, 3)),))
    yield SampleInput(
        make_arg((S, 3, S)), args=(make_arg((S, 3, S)),), kwargs=dict(dim=1)
    )
    yield SampleInput(make_arg((1, 3)), args=(make_arg((S, 3)),), kwargs=dict(dim=-1))

