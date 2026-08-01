
def test__parallel_dict_from_expr_if_gens():
    assert parallel_dict_from_expr([x + 2*y + 3*z, Integer(7)], gens=(x,)) == \
        ([{(1,): Integer(1), (0,): 2*y + 3*z}, {(0,): Integer(7)}], (x,))

