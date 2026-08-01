
def generate_elementwise_binary_tensors(
    op, *, device, dtype, requires_grad=False, exclude_zero=False
):
    shapes = (
        # tensors with no elements
        (0,),
        (1, 0, 3),
        # zero dim (scalar) tensor
        (),
        # small 1D tensor
        (20,),
        # medium 1D tensor
        (812,),
        # large 2D tensor
        (1029, 917),
    )

    make_arg = partial(
        make_tensor,
        device=device,
        dtype=dtype,
        requires_grad=requires_grad,
        exclude_zero=exclude_zero,
    )
    for shape in shapes:
        lhs = make_arg(shape, **op.lhs_make_tensor_kwargs)
        rhs = make_arg(shape, **op.rhs_make_tensor_kwargs)
        yield SampleInput(
            lhs, args=(rhs,), kwargs=op.sample_kwargs(device, dtype, lhs)[0]
        )

