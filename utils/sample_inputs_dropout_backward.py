
def sample_inputs_dropout_backward(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    make_mask = partial(make_tensor, device=device, dtype=torch.bool, requires_grad=False)

    cases = ((S, S, S, S), (S,), ())
    scale_vals = [0.0, 1.0, 2.0]

    for case, scale in product(cases, scale_vals):
        yield SampleInput(make_arg(case), make_mask(case), scale)

