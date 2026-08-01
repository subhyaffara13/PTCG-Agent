
def test_PolyElement_sqf_norm():
    R, x = ring("x", QQ.algebraic_field(sqrt(3)))
    X = R.to_ground().x

    assert (x**2 - 2).sqf_norm() == ([1], x**2 - 2*sqrt(3)*x + 1, X**4 - 10*X**2 + 1)

    R, x = ring("x", QQ.algebraic_field(sqrt(2)))
    X = R.to_ground().x

    assert (x**2 - 3).sqf_norm() == ([1], x**2 - 2*sqrt(2)*x - 1, X**4 - 10*X**2 + 1)

