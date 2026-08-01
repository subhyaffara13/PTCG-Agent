
def sample_inputs_item(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=False)

    cases = (
        (),
        (()),
        (1),
        ((1,)),
    )

    for shape in cases:
        yield SampleInput(make_arg(shape))

