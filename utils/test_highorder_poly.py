
def test_highorder_poly():
    # just testing that the uniq generator is unpacked
    sol = solve(x**6 - 2*x + 2)
    assert all(isinstance(i, CRootOf) for i in sol) and len(sol) == 6

