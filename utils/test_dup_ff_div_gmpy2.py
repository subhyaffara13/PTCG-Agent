
def test_dup_ff_div_gmpy2():
    if GROUND_TYPES != 'gmpy2':
        return

    from gmpy2 import mpq
    from sympy.polys.domains import GMPYRationalField
    K = GMPYRationalField()

    f = [mpq(1,3), mpq(3,2)]
    g = [mpq(2,1)]
    assert dmp_ff_div(f, g, 0, K) == ([mpq(1,6), mpq(3,4)], [])

    f = [mpq(1,2), mpq(1,3), mpq(1,4), mpq(1,5)]
    g = [mpq(-1,1), mpq(1,1), mpq(-1,1)]
    assert dmp_ff_div(f, g, 0, K) == ([mpq(-1,2), mpq(-5,6)], [mpq(7,12), mpq(-19,30)])

