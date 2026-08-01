
def test_tgsyl_NAG(a, b, c, d, e, f, rans, lans, dtype):
    atol = 1e-4

    tgsyl = get_lapack_funcs(('tgsyl'), dtype=dtype)
    rout, lout, scale, dif, info = tgsyl(a, b, c, d, e, f)

    assert_equal(info, 0)
    assert_allclose(scale, 1.0, rtol=0, atol=np.finfo(dtype).eps*100,
                    err_msg="SCALE must be 1.0")
    assert_allclose(dif, 0.0, rtol=0, atol=np.finfo(dtype).eps*100,
                    err_msg="DIF must be nearly 0")
    assert_allclose(rout, rans, atol=atol,
                    err_msg="Solution for R is incorrect")
    assert_allclose(lout, lans, atol=atol,
                    err_msg="Solution for L is incorrect")

