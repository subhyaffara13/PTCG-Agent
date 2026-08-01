
def sample_inputs_singular_matrix_factors(op_info, device, dtype, requires_grad=False):
    """
    This function produces two tensors of shape (*, m, k) and (*, n, k) with k <= min(m, n).
    Their matrix product could be used to generate tensor of shape (*, m, n) of rank k.
    """

    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    batches = [(), (2,)]
    size = [3, 4]
    for batch, m, n in product(batches, size, size):
        k = 2
        a = make_arg((*batch, m, k))
        b = make_arg((*batch, n, k))
        yield a, b

