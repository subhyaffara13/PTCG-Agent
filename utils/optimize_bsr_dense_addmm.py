
def optimize_bsr_dense_addmm(
    m,
    k,
    n,
    bm,
    bk,
    beta=1,
    alpha=1,
    use_left_alpha=False,
    use_right_alpha=False,
    dtype=torch.float16,
    out_dtype=None,
    device="cuda",
    sparsity=0.5,
    force=False,
    verbose=False,
    opname=None,
):
    torch.manual_seed(0)
    bsr = create_blocked_tensor(
        0, m, k, (bm, bk), sparsity, dtype, device
    ).to_sparse_bsr((bm, bk))
    dense = make_tensor(k, n, dtype=dtype, device=device)
    input = make_tensor(m, n, dtype=dtype, device=device)
    left_alpha = make_tensor(m, dtype=dtype, device=device) if use_left_alpha else None
    right_alpha = (
        make_tensor(n, dtype=dtype, device=device) if use_right_alpha else None
    )
    if out_dtype is not None:
        out = dense.new_empty((m, n), dtype=out_dtype)
    else:
        out = None
    tune_bsr_dense_addmm(
        input,
        bsr,
        dense,
        beta=beta,
        alpha=alpha,
        left_alpha=left_alpha,
        right_alpha=right_alpha,
        out=out,
        store=True,
        force=force,
        verbose=verbose,
        opname=opname,
    )

