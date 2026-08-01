
def test_determine_lo_dtype_from_matvec(test_dtype, xp):
    if "longdouble" in test_dtype.__name__ and not is_numpy(xp):
        pytest.skip("longdoubles are only tested for `np`")
    # gh-19209
    scalar = xp.asarray(np.array(1, dtype=test_dtype))
    def mv(v):
        return xp.stack([scalar * v[0], v[1]])

    lo = interface.LinearOperator((2, 2), matvec=mv, xp=xp)
    # expected dtype depends on if mixed exact-inexact promotion is defined
    # since dtype determination follows the following procedure:
    # - take the dtype from calling `matvec` on an `int8`
    # - unless that fails (e.g. via overflow or no mixed exact-inexact promotion),
    #   in which case use the default integral dtype
    expected = scalar.dtype
    if xp.isdtype(expected, ("real floating", "complex floating")):
        try:
            xp.asarray(2) + xp.asarray(2.0)
        except TypeError:
            expected = xpx.default_dtype(xp, kind="integral")
    assert lo.dtype == expected

