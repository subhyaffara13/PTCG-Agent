
def generate_elementwise_binary_with_scalar_and_type_promotion_samples(
    op, *, device, dtype, requires_grad=False
):
    # add these samples only for logical and comparison ops, arithmetic ops are not happy about extremal scalars
    if op.name in (
        "eq",
        "ne",
        "gt",
        "ge",
        "lt",
        "le",
        "logical_and",
        "logical_or",
        "logical_xor",
    ):
        make_arg = partial(
            make_tensor, device=device, dtype=dtype, requires_grad=requires_grad
        )
        shape = (
            23,
        )  # this shape is big enough to trigger vectorization, and has non-vectorized tail
        values = (float("nan"), float("inf"), -float("inf"))
        scalar_tensors = tuple(torch.tensor(val) for val in values)
        if op.supports_rhs_python_scalar:
            lhs = make_arg(shape, **op.lhs_make_tensor_kwargs)
            rhs = make_arg(shape, **op.rhs_make_tensor_kwargs)
            for scalar in values + scalar_tensors:
                yield SampleInput(
                    lhs, args=(scalar,), kwargs=op.sample_kwargs(device, dtype, lhs)[0]
                )
                # Extends with scalar lhs
                if op.supports_one_python_scalar:
                    yield SampleInput(
                        scalar,
                        args=(rhs,),
                        kwargs=op.sample_kwargs(device, dtype, scalar)[0],
                    )

