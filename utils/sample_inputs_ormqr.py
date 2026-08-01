
def sample_inputs_ormqr(op_info, device, dtype, requires_grad, **kwargs):
    # create a helper function wrapping `make_tensor`
    make_input = partial(make_tensor, dtype=dtype, device=device, low=-1, high=1)

    batches = [(), (0, ), (2, ), (2, 1)]
    ns = [5, 2, 0]
    tf = [True, False]
    for batch, (m, n), left, transpose in product(batches, product(ns, ns), tf, tf):
        input = make_input((*batch, m, n))
        reflectors, tau = torch.geqrf(input)
        reflectors.requires_grad_(requires_grad)
        tau.requires_grad_(requires_grad)
        other_matrix_shape = (m, n) if left else (n, m)
        other = make_input((*batch, *other_matrix_shape), requires_grad=requires_grad)
        yield SampleInput(reflectors, tau, other, left=left, transpose=transpose)

