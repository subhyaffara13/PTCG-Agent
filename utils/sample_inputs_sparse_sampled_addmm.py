import itertools

def sample_inputs_sparse_sampled_addmm(op_info, device, dtype, requires_grad, **kwargs):
    alpha = 2 + 3j if dtype.is_complex else 0.6
    beta = 1 + 2j if dtype.is_complex else 0.2
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # sparse.sampled_addmm performs: alpha * (A @ B) * sparse_ones_like(C) + beta * C
    for m, n, k in itertools.product([0, 5], repeat=3):
        yield SampleInput(
            torch.eye(m, n, device=device, dtype=dtype)
            .to_sparse_csr()
            .requires_grad_(requires_grad),
            make_arg((m, k)),
            make_arg((k, n)),
            alpha=alpha,
            beta=beta,
        )

