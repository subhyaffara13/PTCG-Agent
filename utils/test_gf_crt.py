
def test_gf_crt():
    U = [49, 76, 65]
    M = [99, 97, 95]

    p = 912285
    u = 639985

    assert gf_crt(U, M, ZZ) == u

    E = [9215, 9405, 9603]
    S = [62, 24, 12]

    assert gf_crt1(M, ZZ) == (p, E, S)
    assert gf_crt2(U, M, p, E, S, ZZ) == u

