
def sample_inputs_flip(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    sizes = ((S, M, S), (S, 0, M))
    all_dims = ((0, 1, 2), (0,), (0, 2), (-1,), ())

    for size, dims in product(sizes, all_dims):
        yield SampleInput(make_arg(size), kwargs={"dims": dims})

