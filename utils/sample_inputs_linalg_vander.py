
def sample_inputs_linalg_vander(op_info, device, dtype, requires_grad=False, **kwargs):
    make_arg = partial(
        make_tensor, dtype=dtype, device=device, requires_grad=requires_grad
    )

    shapes = (
        (),
        (1,),
        (S,),
        (2, S),
    )

    for shape in shapes:
        if len(shape) > 0 and shape[-1] > 1:
            yield SampleInput(make_arg(shape))
        n = shape[-1] if len(shape) > 0 else 1
        for i in range(3):
            # n-1, n, n+1
            N = n + i - 1
            if N < 2:
                continue
            yield SampleInput(make_arg(shape), kwargs=dict(N=N))

