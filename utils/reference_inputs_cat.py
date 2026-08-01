
def reference_inputs_cat(op, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_cat_concat(op, device, dtype, requires_grad, **kwargs)

    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # Noncontiguous type promoting tensors
    a = make_arg((3, 4, 2))
    b = make_arg((3, 2, 2), noncontiguous=True, dtype=highest_precision_float(device))
    c = make_arg((3, 3, 2), dtype=torch.float16).permute(1, 0, 2)

    yield SampleInput((a, b, c), kwargs={'dim': 1})

    # Special 1D tensor with dim length of 0 case
    a = make_arg((0,))
    b = make_arg((3, 2, 2))

    yield SampleInput((a, b, a))
    yield SampleInput((a, a, a))

