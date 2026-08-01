
def tune__int_bsr_dense_addmm(
    input,
    bsr,
    dense,
    *,
    beta=1,
    alpha=1,
    out=None,
    store=False,
    verbose=False,
    force=False,
):
    return tune_bsr_dense_addmm(
        input,
        bsr,
        dense,
        beta=beta,
        alpha=alpha,
        out=out,
        store=store,
        verbose=verbose,
        force=force,
        opname="_int_bsr_dense_addmm",
    )

