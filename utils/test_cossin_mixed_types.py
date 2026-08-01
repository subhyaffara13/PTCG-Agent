
def test_cossin_mixed_types():
    rng = default_rng(1708093736390459)
    x = np.array(ortho_group.rvs(4, random_state=rng), dtype=np.float64)
    u, cs, vh = cossin([x[:2, :2],
                        np.array(x[:2, 2:], dtype=np.complex128),
                        x[2:, :2],
                        x[2:, 2:]])

    assert u.dtype == np.complex128
    assert cs.dtype == np.float64
    assert vh.dtype == np.complex128
    assert_allclose(x, u @ cs @ vh, rtol=0.,
                    atol=1e4 * np.finfo(np.complex128).eps)

