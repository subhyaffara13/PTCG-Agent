
def test_singleton_dimension_broadcast() -> None:
    # singleton dimensions broadcast (gh-10343)
    p = np.ones((10, 2))
    q = np.ones((1, 2))

    ein = contract("ij,ij->j", p, q, optimize=False)
    opt = contract("ij,ij->j", p, q, optimize=True)
    assert np.allclose(ein, opt)
    assert np.allclose(opt, [10.0, 10.0])

    p = np.ones((1, 5))
    q = np.ones((5, 5))

    for optimize in (True, False):
        res1 = (contract("...ij,...jk->...ik", p, p, optimize=optimize),)
        res2 = contract("...ij,...jk->...ik", p, q, optimize=optimize)
        assert np.allclose(res1, res2)
        assert np.allclose(res2, np.full((1, 5), 5))

