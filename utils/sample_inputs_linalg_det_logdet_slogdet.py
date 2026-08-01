
def sample_inputs_linalg_det_logdet_slogdet(
    op_info, device, dtype, requires_grad, **kwargs
):
    make_fullrank = make_fullrank_matrices_with_distinct_singular_values
    make_arg = partial(
        make_fullrank, dtype=dtype, device=device, requires_grad=requires_grad
    )
    batches = [(), (0,), (3,)]
    ns = [0, 1, 5]

    is_logdet = op_info.name == "logdet"

    for (
        batch,
        n,
    ) in product(batches, ns):
        shape = batch + (n, n)
        A = make_arg(*shape)
        # Need to make the matrices in A have positive determinant for autograd
        # To do so, we multiply A by its determinant to flip the sign of its determinant
        if is_logdet and not A.is_complex() and A.numel() > 0:
            s = torch.linalg.slogdet(A).sign
            A = A * s.unsqueeze(-1).unsqueeze(-1)
            A.requires_grad_(requires_grad)
        yield SampleInput(A)

