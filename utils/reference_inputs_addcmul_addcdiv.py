
def reference_inputs_addcmul_addcdiv(op_info, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_addcmul_addcdiv(
        op_info, device, dtype, requires_grad, **kwargs)

    # type promotion cases
    supported_dtypes = op_info.supported_dtypes(device)
    make_arg = partial(make_tensor, device=device, requires_grad=requires_grad)

    types = (
        (torch.float64, torch.complex128),
        (torch.bfloat16, torch.float32),
    )

    values = (
        None,
        True, False,
        3.14, 3,
        1.0, 1,
        0.0, 0,
        -3.14, -3,
        3.14 + 2.71j,
    )

    for (type2, type3), value in product(types, values):
        if (type2 not in supported_dtypes or
                type3 not in supported_dtypes):
            continue

        # RuntimeError: value cannot be converted without overflow
        if (type(value) is complex and
                type2 is not torch.complex128):
            continue

        arg1 = make_arg([5, 5], dtype=dtype)
        arg2 = make_arg([5, 5], dtype=type2)
        arg3 = make_arg([1, 5], dtype=type3)

        # TypeError: addcdiv(): argument 'value' must be Number, not NoneType
        if value is not None:
            yield SampleInput(arg1, args=(arg2, arg3), kwargs=dict(value=value))
        else:
            yield SampleInput(arg1, args=(arg2, arg3))

