import random

def test_jcn():
    """
    Test some special cases of the cn(z, q) function.
    """
    mp.dps = 100

    # Abramowitz Table 16.5
    # cn(0, q) = 1
    qstring = str(random.random())
    q = mpf(qstring)
    cn = jcn(zero, q)
    assert(cn.ae(one))

    # Abramowitz Table 16.6.2
    #
    # cn(u, 0) = cos(u), m == 0
    #
    # cn(u, 1) = sech(z), m == 1
    #
    # It would be nice to test these, but I find that they run
    # in to numerical trouble.  I'm currently treating as a boundary
    # case for cn function.

    mp.dps = 25
    arg = one/10
    m = ldexp(one, -100)
    #N[JacobiCN[1/10, 2^-100], 25]
    res = mpf('0.9950041652780257660955620')
    result = jcn(arg, m)
    assert(result.ae(res))

    # N[JacobiCN[1/10, 1/10], 25]
    res = mpf('0.9950058256237368748520459')
    result = jcn(arg, arg)
    assert(result.ae(res))
    mp.dps = 15

