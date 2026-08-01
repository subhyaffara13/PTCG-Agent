
def test_determine_lo_dtype_for_int(xp):
    # gh-19209
    # test Python int larger than int8 max cast to some int
    def mv(v):
        return xp.asarray([128 * v[0], v[1]])

    lo = interface.LinearOperator((2, 2), matvec=mv, xp=xp)
    assert xp.isdtype(lo.dtype, "integral")

