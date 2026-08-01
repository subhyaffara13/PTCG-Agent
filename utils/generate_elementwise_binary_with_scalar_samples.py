
def generate_elementwise_binary_with_scalar_samples(
    op, *, device, dtype, requires_grad=False
):
    make_arg = partial(
        make_tensor, device=device, dtype=dtype, requires_grad=requires_grad
    )

    shapes = ((), (3,), (5, 3), (0, 1, 3), (1, 5))
    if op.supports_rhs_python_scalar:
        for shape in shapes:
            lhs = make_arg(shape, **op.lhs_make_tensor_kwargs)
            rhs = make_arg(shape, **op.rhs_make_tensor_kwargs)
            lhs_scalar = make_arg((), **op.lhs_make_tensor_kwargs).item()
            rhs_scalar = make_arg((), **op.rhs_make_tensor_kwargs).item()

            yield SampleInput(
                lhs, args=(rhs_scalar,), kwargs=op.sample_kwargs(device, dtype, lhs)[0]
            )

        # Extends with scalar lhs
        if op.supports_one_python_scalar:
            yield SampleInput(
                lhs_scalar,
                args=(rhs,),
                kwargs=op.sample_kwargs(device, dtype, lhs_scalar)[0],
            )

    if op.supports_two_python_scalars:
        lhs_scalar = make_arg((), **op.lhs_make_tensor_kwargs).item()
        rhs_scalar = make_arg((), **op.rhs_make_tensor_kwargs).item()

        yield SampleInput(
            lhs_scalar,
            args=(rhs_scalar,),
            kwargs=op.sample_kwargs(device, dtype, lhs_scalar)[0],
        )

