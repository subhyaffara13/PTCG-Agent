
def test_trexc_NAG(t, ifst, ilst, expect):
    """
    This test implements the example found in the NAG manual,
    f08qfc, f08qtc, f08qgc, f08quc.
    """
    # NAG manual provides accuracy up to 4 decimals
    atol = 1e-4
    trexc = get_lapack_funcs('trexc', dtype=t.dtype)

    result = trexc(t, t, ifst, ilst, wantq=0)
    assert_equal(result[-1], 0)

    t = result[0]
    assert_allclose(expect, t, atol=atol)

