
def test_instantiation_evaluation():
    from sympy.abc import v, w, x, y, z
    assert Min(1, Max(2, x)) == 1
    assert Max(3, Min(2, x)) == 3
    assert Min(Max(x, y), Max(x, z)) == Max(x, Min(y, z))
    assert set(Min(Max(w, x), Max(y, z)).args) == {
        Max(w, x), Max(y, z)}
    assert Min(Max(x, y), Max(x, z), w) == Min(
        w, Max(x, Min(y, z)))
    A, B = Min, Max
    for i in range(2):
        assert A(x, B(x, y)) == x
        assert A(x, B(y, A(x, w, z))) == A(x, B(y, A(w, z)))
        A, B = B, A
    assert Min(w, Max(x, y), Max(v, x, z)) == Min(
        w, Max(x, Min(y, Max(v, z))))

