
def _reference_inputs_elementwise_binary(
    op, device, dtype, requires_grad, exclude_zero, **kwargs
):
    yield from op.sample_inputs_func(op, device, dtype, requires_grad, **kwargs)
    yield from generate_elementwise_binary_tensors(
        op,
        device=device,
        dtype=dtype,
        requires_grad=requires_grad,
        exclude_zero=exclude_zero,
    )
    if dtype is not torch.bool:
        yield from generate_elementwise_binary_small_value_tensors(
            op, device=device, dtype=dtype, requires_grad=requires_grad
        )
    if dtype not in (torch.bool, torch.uint8, torch.int8):
        yield from generate_elementwise_binary_large_value_tensors(
            op, device=device, dtype=dtype, requires_grad=requires_grad
        )
    yield from generate_elementwise_binary_broadcasting_tensors(
        op,
        device=device,
        dtype=dtype,
        requires_grad=requires_grad,
        exclude_zero=exclude_zero,
    )
    yield from generate_elementwise_binary_with_scalar_samples(
        op, device=device, dtype=dtype, requires_grad=requires_grad
    )

    yield from generate_elementwise_binary_with_scalar_and_type_promotion_samples(
        op, device=device, dtype=dtype, requires_grad=requires_grad
    )

    if dtype.is_floating_point or dtype.is_complex:
        yield from generate_elementwise_binary_extremal_value_tensors(
            op, device=device, dtype=dtype, requires_grad=requires_grad
        )

