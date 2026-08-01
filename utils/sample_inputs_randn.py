
def sample_inputs_randn(op, device, dtype, requires_grad, **kwargs):
    shapes = (
        (M,),
        (S, S)
    )

    for shape in shapes:
        yield SampleInput(input=shape, kwargs=dict(dtype=dtype, device=device, requires_grad=requires_grad))

