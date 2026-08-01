
def sample_inputs_linalg_qr_geqrf(
    op_info, device, dtype, requires_grad=False, **kwargs
):
    # QR is just well defined when the matrix is full rank
    make_fullrank = make_fullrank_matrices_with_distinct_singular_values
    make_arg = partial(
        make_fullrank, dtype=dtype, device=device, requires_grad=requires_grad
    )

    batches = [(), (0,), (2,), (1, 1)]
    ns = [5, 2, 0]

    for batch, (m, n) in product(batches, product(ns, ns)):
        shape = batch + (m, n)
        yield SampleInput(make_arg(*shape))

