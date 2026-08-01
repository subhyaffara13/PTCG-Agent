
def test_laplacian_symmetrized(arr_type, form):
    # adjacency matrix
    n = 3
    mat = arr_type(np.arange(n * n).reshape(n, n))
    L_in, d_in = csgraph.laplacian(
        mat,
        return_diag=True,
        form=form,
    )
    L_out, d_out = csgraph.laplacian(
        mat,
        return_diag=True,
        use_out_degree=True,
        form=form,
    )
    Ls, ds = csgraph.laplacian(
        mat,
        return_diag=True,
        symmetrized=True,
        form=form,
    )
    Ls_normed, ds_normed = csgraph.laplacian(
        mat,
        return_diag=True,
        symmetrized=True,
        normed=True,
        form=form,
    )
    mat += mat.T
    Lss, dss = csgraph.laplacian(mat, return_diag=True, form=form)
    Lss_normed, dss_normed = csgraph.laplacian(
        mat,
        return_diag=True,
        normed=True,
        form=form,
    )

    assert_allclose(ds, d_in + d_out)
    assert_allclose(ds, dss)
    assert_allclose(ds_normed, dss_normed)

    d = {}
    for L in ["L_in", "L_out", "Ls", "Ls_normed", "Lss", "Lss_normed"]:
        if form == "array":
            d[L] = eval(L)
        else:
            d[L] = eval(L)(np.eye(n, dtype=mat.dtype))

    _assert_allclose_sparse(d["Ls"], d["L_in"] + d["L_out"].T)
    _assert_allclose_sparse(d["Ls"], d["Lss"])
    _assert_allclose_sparse(d["Ls_normed"], d["Lss_normed"])

