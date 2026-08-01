
def test_ptsvx_NAG(d, e, b, x):
    # test to assure that wrapper is consistent with NAG Manual Mark 26
    # example problems: f07jbf, f07jpf
    # (Links expire, so please search for "NAG Library Manual Mark 26" online)

    # obtain routine with correct type based on e.dtype
    ptsvx = get_lapack_funcs('ptsvx', dtype=e.dtype)
    # solve using routine
    df, ef, x_ptsvx, rcond, ferr, berr, info = ptsvx(d, e, b)
    # determine ptsvx's solution and x are the same.
    assert_array_almost_equal(x, x_ptsvx)

