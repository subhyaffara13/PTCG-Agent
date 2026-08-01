
def sample_inputs_view_reshape(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    cases = (
        # a, b, is_tensor_supported
        ((S, S, S), (S * S, S), True),
        ((S * S, S), (S, S, S), True),
        ((S * S, S), (S, -1, S), False),  # neg index
        ((S * S * 2, S), (S, -1), False),  # neg index
        ((S,), (S,), True),
        ((), (), False),  # empty
        ((), (1,), True),
    )

    for a, b, is_tensor_supported in cases:
        # skip unsupported cases
        if kwargs.get("tensor_arg") and not is_tensor_supported:
            continue

        # convert to tensor
        if kwargs.get("tensor_arg"):
            b = make_arg(b, requires_grad=False)

        yield SampleInput(make_arg(a), args=(b,))

