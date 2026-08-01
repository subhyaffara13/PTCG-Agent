
def generate_elementwise_binary_extremal_value_tensors(
    op, *, device, dtype, requires_grad=False
):
    _float_extremals = (float("inf"), float("-inf"), float("nan"))

    l_vals = []
    r_vals = []

    if dtype.is_floating_point:
        prod = product(_float_extremals, _float_extremals)
    elif dtype.is_complex:
        complex_vals = product(_float_extremals, _float_extremals)
        # Note the use of list is required here or the map generator will be
        #  emptied by the following product and it won't produce the desired cross-product
        complex_vals = [complex(*x) for x in complex_vals]
        prod = product(complex_vals, complex_vals)
    else:
        raise ValueError("Unsupported dtype!")

    for l, r in prod:
        l_vals.append(l)
        r_vals.append(r)

    lhs = torch.tensor(l_vals, device=device, dtype=dtype, requires_grad=requires_grad)
    rhs = torch.tensor(r_vals, device=device, dtype=dtype, requires_grad=requires_grad)

    yield SampleInput(lhs, args=(rhs,), kwargs=op.sample_kwargs(device, dtype, lhs)[0])

    # Test case for NaN propagation
    nan = (
        float("nan") if dtype.is_floating_point else complex(float("nan"), float("nan"))
    )
    lhs = make_tensor(
        (128, 128), device=device, dtype=dtype, requires_grad=requires_grad
    )
    lhs.view(-1)[::3] = nan
    rhs = make_tensor(
        (128, 128), device=device, dtype=dtype, requires_grad=requires_grad
    )
    rhs.view(-1)[::3] = nan

    yield SampleInput(lhs, args=(rhs,), kwargs=op.sample_kwargs(device, dtype, lhs)[0])

