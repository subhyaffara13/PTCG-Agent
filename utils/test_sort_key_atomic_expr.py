
def test_sort_key_atomic_expr():
    from sympy.physics.units import m, s
    assert sorted([-m, s], key=lambda arg: arg.sort_key()) == [-m, s]

