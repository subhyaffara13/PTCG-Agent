
def _generate_sample_inputs_nn_loss(op_info, device, dtype, requires_grad, **kwargs):
    _make_tensor = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    for s, r in _generate_sample_shape_reduction():
        yield _make_tensor(s), _make_tensor(s), dict(reduction=r)

