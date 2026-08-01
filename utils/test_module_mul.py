
def test_module_mul():
    R = QQ.old_poly_ring(x)
    M = R.free_module(2)
    S1 = M.submodule([x, 0], [0, x])
    S2 = M.submodule([x**2, 0], [0, x**2])
    I = R.ideal(x)

    assert I*M == M*I == S1 == x*M == M*x
    assert I*S1 == S2 == x*S1

