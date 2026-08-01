
def test_dmp_integrate_in():
    f = dmp_convert(f_6, 3, ZZ, QQ)

    assert dmp_integrate_in(f, 2, 1, 3, QQ) == \
        dmp_swap(
            dmp_integrate(dmp_swap(f, 0, 1, 3, QQ), 2, 3, QQ), 0, 1, 3, QQ)
    assert dmp_integrate_in(f, 3, 1, 3, QQ) == \
        dmp_swap(
            dmp_integrate(dmp_swap(f, 0, 1, 3, QQ), 3, 3, QQ), 0, 1, 3, QQ)
    assert dmp_integrate_in(f, 2, 2, 3, QQ) == \
        dmp_swap(
            dmp_integrate(dmp_swap(f, 0, 2, 3, QQ), 2, 3, QQ), 0, 2, 3, QQ)
    assert dmp_integrate_in(f, 3, 2, 3, QQ) == \
        dmp_swap(
            dmp_integrate(dmp_swap(f, 0, 2, 3, QQ), 3, 3, QQ), 0, 2, 3, QQ)

    raises(IndexError, lambda: dmp_integrate_in(f, 1, -1, 3, QQ))
    raises(IndexError, lambda: dmp_integrate_in(f, 1, 4, 3, QQ))

