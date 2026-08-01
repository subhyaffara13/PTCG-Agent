
def sample_inputs_mvlgamma(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    tensor_shapes = ((S, S), ())
    ns = (1, 2, 3, 4, 5)

    # Since the accepted lower bound for input
    # to mvlgamma depends on `p` argument,
    # the following function computes the lower bound
    # which we pass to `make_tensor`.
    def compute_min_val(p):
        return (p - 1.) / 2

    for shape, n in product(tensor_shapes, ns):
        min_val = compute_min_val(n)
        if not dtype.is_floating_point:
            # Round-up minimum value for integral dtypes
            min_val += 1
        else:
            min_val += 2 * torch.finfo(dtype).eps
        yield SampleInput(make_arg(shape, low=min_val), args=(n,))

