
def sample_inputs_polygamma(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(
        make_tensor,
        device=device,
        # TODO: eliminate low after gh-106692 is fixed:
        low=(1 if dtype in {torch.int32, torch.int64} else None),
        dtype=dtype,
        requires_grad=requires_grad,
    )
    tensor_shapes = ((S, S), ())
    ns = (1, 2, 3, 4, 5)

    for shape, n in product(tensor_shapes, ns):
        yield SampleInput(make_arg(shape), args=(n,))

