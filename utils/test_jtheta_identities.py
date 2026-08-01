
def test_jtheta_identities():
    """
    Tests the some of the jacobi identidies found in Abramowitz,
    Sec. 16.28, Pg. 576. The identities are tested to 1 part in 10^98.
    """
    mp.dps = 110
    eps1 = ldexp(eps, 30)

    for i in range(10):
        qstring = str(random.random())
        q = mpf(qstring)

        zstring = str(10*random.random())
        z = mpf(zstring)
        # Abramowitz 16.28.1
        # v_1(z, q)**2 * v_4(0, q)**2 =   v_3(z, q)**2 * v_2(0, q)**2
        #                               - v_2(z, q)**2 * v_3(0, q)**2
        term1 = (jtheta(1, z, q)**2) * (jtheta(4, zero, q)**2)
        term2 = (jtheta(3, z, q)**2) * (jtheta(2, zero, q)**2)
        term3 = (jtheta(2, z, q)**2) * (jtheta(3, zero, q)**2)
        equality = term1 - term2 + term3
        assert(equality.ae(0, eps1))

        zstring = str(100*random.random())
        z = mpf(zstring)
        # Abramowitz 16.28.2
        # v_2(z, q)**2 * v_4(0, q)**2 =   v_4(z, q)**2 * v_2(0, q)**2
        #                               - v_1(z, q)**2 * v_3(0, q)**2
        term1 = (jtheta(2, z, q)**2) * (jtheta(4, zero, q)**2)
        term2 = (jtheta(4, z, q)**2) * (jtheta(2, zero, q)**2)
        term3 = (jtheta(1, z, q)**2) * (jtheta(3, zero, q)**2)
        equality = term1 - term2 + term3
        assert(equality.ae(0, eps1))

        # Abramowitz 16.28.3
        # v_3(z, q)**2 * v_4(0, q)**2 =   v_4(z, q)**2 * v_3(0, q)**2
        #                               - v_1(z, q)**2 * v_2(0, q)**2
        term1 = (jtheta(3, z, q)**2) * (jtheta(4, zero, q)**2)
        term2 = (jtheta(4, z, q)**2) * (jtheta(3, zero, q)**2)
        term3 = (jtheta(1, z, q)**2) * (jtheta(2, zero, q)**2)
        equality = term1 - term2 + term3
        assert(equality.ae(0, eps1))

        # Abramowitz 16.28.4
        # v_4(z, q)**2 * v_4(0, q)**2 =   v_3(z, q)**2 * v_3(0, q)**2
        #                               - v_2(z, q)**2 * v_2(0, q)**2
        term1 = (jtheta(4, z, q)**2) * (jtheta(4, zero, q)**2)
        term2 = (jtheta(3, z, q)**2) * (jtheta(3, zero, q)**2)
        term3 = (jtheta(2, z, q)**2) * (jtheta(2, zero, q)**2)
        equality = term1 - term2 + term3
        assert(equality.ae(0, eps1))

        # Abramowitz 16.28.5
        # v_2(0, q)**4 + v_4(0, q)**4 == v_3(0, q)**4
        term1 = (jtheta(2, zero, q))**4
        term2 = (jtheta(4, zero, q))**4
        term3 = (jtheta(3, zero, q))**4
        equality = term1 + term2 - term3
        assert(equality.ae(0, eps1))
    mp.dps = 15

