
def sample_inputs_dist(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    sizes = ((S, S, S), (S,), (S, 1, S), (), (S, S))
    ps = (2, 4)

    for size_x, size_y, p in product(sizes, sizes, ps):
        yield SampleInput(make_arg(size_x), args=(make_arg(size_y), p))

