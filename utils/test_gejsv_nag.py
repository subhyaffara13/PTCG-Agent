
def test_gejsv_NAG(A, sva_expect, u_expect, v_expect):
    """
    This test implements the example found in the NAG manual, f08khf.
    An example was not found for the complex case.
    """
    # NAG manual provides accuracy up to 4 decimals
    atol = 1e-4
    gejsv = get_lapack_funcs('gejsv', dtype=A.dtype)

    sva, u, v, work, iwork, info = gejsv(A)

    assert_allclose(sva_expect, sva, atol=atol)
    assert_allclose(u_expect, u, atol=atol)
    assert_allclose(v_expect, v, atol=atol)

