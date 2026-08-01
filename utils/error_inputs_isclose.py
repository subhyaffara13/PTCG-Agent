
def error_inputs_isclose(op, device, **kwargs):
    make_float_arg = partial(make_tensor, device=device, dtype=torch.float, requires_grad=False)

    yield ErrorInput(SampleInput(make_float_arg(()), args=(make_float_arg(()),), kwargs={'rtol': -0.4}),
                     error_type=RuntimeError,
                     error_regex='rtol must be greater than or equal to zero')

    yield ErrorInput(SampleInput(make_float_arg(()), args=(make_float_arg(()),), kwargs={'atol': -0.4}),
                     error_type=RuntimeError,
                     error_regex='atol must be greater than or equal to zero')

