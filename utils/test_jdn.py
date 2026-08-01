
def test_jdn():
    """
    Test some special cases of the dn(z, q) function.
    """
    mp.dps = 100

    # Abramowitz Table 16.5
    # dn(0, q) = 1
    mstring = str(random.random())
    m = mpf(mstring)

    dn = jdn(zero, m)
    assert(dn.ae(one))

    mp.dps = 25
    # N[JacobiDN[1/10, 1/10], 25]
    res = mpf('0.9995017055025556219713297')
    arg = one/10
    result = jdn(arg, arg)
    assert(result.ae(res))
    mp.dps = 15

