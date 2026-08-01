
def test__parallel_dict_from_expr_no_gens():
    assert parallel_dict_from_expr([x*y, Integer(3)]) == \
        ([{(1, 1): Integer(1)}, {(0, 0): Integer(3)}], (x, y))
    assert parallel_dict_from_expr([x*y, 2*z, Integer(3)]) == \
        ([{(1, 1, 0): Integer(
            1)}, {(0, 0, 1): Integer(2)}, {(0, 0, 0): Integer(3)}], (x, y, z))
    assert parallel_dict_from_expr((Mul(x, x**2, evaluate=False),)) == \
        ([{(3,): 1}], (x,))

