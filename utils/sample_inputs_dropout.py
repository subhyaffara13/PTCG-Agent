
def sample_inputs_dropout(op_info, device, dtype, requires_grad, *,
                          train=None, valid_input_dim=None, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    if valid_input_dim:
        cases = ((S,) * i for i in valid_input_dim)
    else:
        cases = ((S, S), (S,), ())
    p_vals = [0.0, 0.5, 1.0]
    # This is to handle special case for feature_alpha_dropout which has different
    # supported dtypes depending on `train` parameter
    training_vals = [train] if train is not None else [True, False]

    for case, p, training in product(cases, p_vals, training_vals):
        yield SampleInput(make_arg(case), p=p, training=training)
    yield SampleInput(make_arg(case))

