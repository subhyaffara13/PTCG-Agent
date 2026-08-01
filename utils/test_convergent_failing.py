
def test_convergent_failing():
    # dirichlet tests
    assert Sum(sin(n)/n, (n, 1, oo)).is_convergent() is S.true
    assert Sum(sin(2*n)/n, (n, 1, oo)).is_convergent() is S.true

