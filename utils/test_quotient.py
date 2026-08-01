
def test_quotient():
    # SCA, example 1.8.13
    R = QQ.old_poly_ring(x, y, z)
    assert R.ideal(x, y).quotient(R.ideal(y**2, z)) == R.ideal(x, y)


def test_quotient():
    # SCA, example 2.8.6
    R = QQ.old_poly_ring(x, y, z)
    F = R.free_module(2)
    assert F.submodule([x*y, x*z], [y*z, x*y]).module_quotient(
        F.submodule([y, z], [z, y])) == QQ.old_poly_ring(x, y, z).ideal(x**2*y**2 - x*y*z**2)
    assert F.submodule([x, y]).module_quotient(F.submodule()).is_whole_ring()

    M = F.submodule([x**2, x**2], [y**2, y**2])
    N = F.submodule([x + y, x + y])
    q, rel = M.module_quotient(N, relations=True)
    assert q == R.ideal(y**2, x - y)
    for i, g in enumerate(q.gens):
        assert g*N.gens[0] == sum(c*x for c, x in zip(rel[i], M.gens))

