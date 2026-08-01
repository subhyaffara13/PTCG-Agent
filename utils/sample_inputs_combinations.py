
def sample_inputs_combinations(op_info, device, dtype, requires_grad, **kwargs):
    inputs = (
        (0,),
        (0, 1),
        (0, 1, 2, 3),
    )

    rvals = [1, 2, 4]

    products = product(inputs, rvals, [False, True])

    for input_data, r, with_replacement in products:
        input_t = torch.tensor(input_data, device=device, dtype=dtype, requires_grad=requires_grad)
        yield SampleInput(input_t, r=r, with_replacement=with_replacement)

