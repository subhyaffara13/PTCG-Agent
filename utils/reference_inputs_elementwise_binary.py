
def reference_inputs_elementwise_binary(op, device, dtype, requires_grad, **kwargs):
    if hasattr(op, "rhs_make_tensor_kwargs"):
        exclude_zero = op.rhs_make_tensor_kwargs.get("exclude_zero", False)

    gen = partial(
        _reference_inputs_elementwise_binary,
        op,
        device,
        dtype,
        requires_grad,
        exclude_zero,
        **kwargs,
    )

    # yields "normal" samples
    yield from gen()

    # yields noncontiguous samples
    for sample in gen():
        yield sample.noncontiguous()

    yield from generate_elementwise_binary_noncontiguous_tensors(
        op,
        device=device,
        dtype=dtype,
        requires_grad=requires_grad,
        exclude_zero=exclude_zero,
    )

    yield from generate_elementwise_binary_arbitrarily_strided_tensors(
        op,
        device=device,
        dtype=dtype,
        requires_grad=requires_grad,
        exclude_zero=exclude_zero,
    )

