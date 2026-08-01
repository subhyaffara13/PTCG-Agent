
def test_sn_cn_dn_identities():
    """
    Tests the some of the jacobi elliptic function identities found
    on Mathworld. Haven't found in Abramowitz.
    """
    mp.dps = 100
    N = 5
    for i in range(N):
        qstring = str(random.random())
        q = mpf(qstring)
        zstring = str(100*random.random())
        z = mpf(zstring)

        # MathWorld
        # sn(z, q)**2 + cn(z, q)**2 == 1
        term1 = jsn(z, q)**2
        term2 = jcn(z, q)**2
        equality = one - term1 - term2
        assert(equality.ae(0))

    # MathWorld
    # k**2 * sn(z, m)**2 + dn(z, m)**2 == 1
    for i in range(N):
        mstring = str(random.random())
        m = mpf(qstring)
        k = m.sqrt()
        zstring = str(10*random.random())
        z = mpf(zstring)
        term1 = k**2 * jsn(z, m)**2
        term2 = jdn(z, m)**2
        equality = one - term1 - term2
        assert(equality.ae(0))


    for i in range(N):
        mstring = str(random.random())
        m = mpf(mstring)
        k = m.sqrt()
        zstring = str(random.random())
        z = mpf(zstring)

        # MathWorld
        # k**2 * cn(z, m)**2 + (1 - k**2) = dn(z, m)**2
        term1 = k**2 * jcn(z, m)**2
        term2 = 1 - k**2
        term3 = jdn(z, m)**2
        equality = term3 - term1 - term2
        assert(equality.ae(0))

        K = ellipk(k**2)
        # Abramowitz Table 16.5
        # sn(K, m) = 1; K is K(k), first complete elliptic integral
        r = jsn(K, m)
        assert(r.ae(one))

        # Abramowitz Table 16.5
        # cn(K, q) = 0; K is K(k), first complete elliptic integral
        equality = jcn(K, m)
        assert(equality.ae(0))

        # Abramowitz Table 16.6.3
        # dn(z, 0) = 1, m == 0
        z = m
        value = jdn(z, zero)
        assert(value.ae(one))

    mp.dps = 15

