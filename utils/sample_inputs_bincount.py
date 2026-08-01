
def sample_inputs_bincount(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    for size, weighted in product((S, M), [False, True]):
        input_tensor = torch.randint(0, size, (size,), dtype=dtype, device=device)
        weight_tensor = make_arg((size,)) if weighted else None

        max_val = int(input_tensor.max().item())

        for minlength in [0, max_val // 2, max_val, 2 * max_val]:
            yield SampleInput(
                input_tensor, weights=weight_tensor, minlength=minlength)

