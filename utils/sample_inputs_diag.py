
def sample_inputs_diag(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad, low=None, high=None)
    yield SampleInput(make_arg(M))

    tensors = (
        make_arg((M, M)),
        make_arg((3, 5)),
        make_arg((5, 3)),
    )

    args = ((), (2,), (-2,), (1,), (2,))

    for tensor, arg in product(tensors, args):
        yield SampleInput(tensor.clone().requires_grad_(requires_grad), *arg)

