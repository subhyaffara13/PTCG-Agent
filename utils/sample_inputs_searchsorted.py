
def sample_inputs_searchsorted(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    # (unsorted tensor size, (input sizes,), is_scalar)
    sizes = (
        ((0,), ((0,),), False),
        ((M,), ((), (M,), (M, M)), False),
        ((0, 0), ((0, 0),), False),
        ((M, M), ((M, M),), False),
        ((0, 0, 0), ((0, 0, 0),), False),
        ((M, M, M), ((M, M, M),), False),
        ((L,), ((),), True),
    )

    for (size, input_sizes, is_scalar), noncontiguous, out_int32, right in product(
        sizes, [False, True], [False, True], [False, True]
    ):
        unsorted_tensor = make_arg(size, noncontiguous=noncontiguous)
        for input_size in input_sizes:
            input = make_arg(input_size, noncontiguous=noncontiguous)
            if is_scalar:
                input = input.item()
            if np.prod(size) == 0:
                boundary_tensor = unsorted_tensor
                sorter = make_tensor(size, dtype=torch.int64, device=device, noncontiguous=noncontiguous)
            else:
                boundary_tensor, sorter = torch.sort(unsorted_tensor)
            side = "right" if right else "left"

            yield SampleInput(boundary_tensor, input, out_int32=out_int32, right=right)
            yield SampleInput(boundary_tensor, input, out_int32=out_int32, side=side)

            yield SampleInput(unsorted_tensor, input, out_int32=out_int32, right=right, sorter=sorter)
            yield SampleInput(unsorted_tensor, input, out_int32=out_int32, side=side, sorter=sorter)

