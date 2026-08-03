import random

def test_jsn():
    """
    Test some special cases of the sn(z, q) function.
    """
    mp.dps = 100

    # trival case
    result = jsn(zero, zero)
    assert(result == zero)

    # Abramowitz Table 16.5
    #
    # sn(0, m) = 0

    for i in range(10):
        qstring = str(random.random())
        q = mpf(qstring)

        equality = jsn(zero, q)
        assert(equality.ae(0))

    # Abramowitz Table 16.6.1
    #
    # sn(z, 0) = sin(z), m == 0
    #
    # sn(z, 1) = tanh(z), m == 1
    #
    # It would be nice to test these, but I find that they run
    # in to numerical trouble.  I'm currently treating as a boundary
    # case for sn function.

    mp.dps = 25
    arg = one/10
    #N[JacobiSN[1/10, 2^-100], 25]
    res = mpf('0.09983341664682815230681420')
    m = ldexp(one, -100)
    result = jsn(arg, m)
    assert(result.ae(res))

    # N[JacobiSN[1/10, 1/10], 25]
    res = mpf('0.09981686718599080096451168')
    result = jsn(arg, arg)
    assert(result.ae(res))
    mp.dps = 15

