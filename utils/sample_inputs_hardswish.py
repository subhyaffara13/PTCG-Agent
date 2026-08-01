
def sample_inputs_hardswish(self, device, dtype, requires_grad, **kwargs):
    N = 5
    # make sure we are testing -3 -> 3 range. default is -10 -> 10 so maybe unnecessary ?
    make_arg = partial(make_tensor, device=device, dtype=dtype,
                       requires_grad=requires_grad, low=-5, high=5)
    return (SampleInput(make_arg((N * 2, N * 2))) for _ in range(1, N))

