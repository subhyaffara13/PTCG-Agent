
def sample_inputs_softmax_backward_data(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(
        make_tensor, device=device, dtype=dtype, requires_grad=requires_grad
    )
    cases = [
        ((S,), 0),
        ((S, S), 0),
        ((S, M, S), -1),
    ]
    input_dtypes = [dtype]
    if dtype == torch.float and device == 'cuda':
        input_dtypes += [torch.float16]

    for (shape, dim), input_dtype in product(cases, input_dtypes):
        input = make_arg(shape)
        output = torch.nn.functional.softmax(input, dim=dim, dtype=input_dtype)
        yield SampleInput(make_arg(shape), output, dim, input_dtype)

