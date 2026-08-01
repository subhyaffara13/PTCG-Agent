
def test_format():
    assert '{:1.2f}'.format(S.Zero) == '0.00'
    assert '{:+3.0f}'.format(S(3)) == ' +3'
    assert '{:23.20f}'.format(pi) == ' 3.14159265358979323846'
    assert '{:50.48f}'.format(exp(sin(1))) == '2.319776824715853173956590377503266813254904772376'


def test_format(dtype, arr_type, normed, symmetrized, use_out_degree, form):
    n = 3
    mat = [[0, 1, 0], [4, 2, 0], [0, 0, 0]]
    mat = arr_type(np.array(mat), dtype=dtype)
    Lo, do = csgraph.laplacian(
        mat,
        return_diag=True,
        normed=normed,
        symmetrized=symmetrized,
        use_out_degree=use_out_degree,
        dtype=dtype,
    )
    La, da = csgraph.laplacian(
        mat,
        return_diag=True,
        normed=normed,
        symmetrized=symmetrized,
        use_out_degree=use_out_degree,
        dtype=dtype,
        form="array",
    )
    assert_allclose(do, da)
    _assert_allclose_sparse(Lo, La)

    L, d = csgraph.laplacian(
        mat,
        return_diag=True,
        normed=normed,
        symmetrized=symmetrized,
        use_out_degree=use_out_degree,
        dtype=dtype,
        form=form,
    )
    assert_allclose(d, do)
    assert d.dtype == dtype
    Lm = L(np.eye(n, dtype=mat.dtype)).astype(dtype)
    _assert_allclose_sparse(Lm, Lo, rtol=2e-7, atol=2e-7)
    x = np.arange(6).reshape(3, 2)
    if not (normed and dtype in INT_DTYPES):
        assert_allclose(L(x), Lo @ x)
    else:
        # Normalized Lo is casted to integer, but L() is not
        pass


def test_format():
    # GH-34740
    assert format(NA) == "<NA>"
    assert format(NA, ">10") == "      <NA>"
    assert format(NA, "xxx") == "<NA>"  # NA is flexible, accept any format spec

    assert f"{NA}" == "<NA>"
    assert f"{NA:>10}" == "      <NA>"
    assert f"{NA:xxx}" == "<NA>"


def test_format():
    assert_(f"{1 + LD_INFO.eps:.40g}" != '1')

