
def test_local_dict_split_implmult():
    t = standard_transformations + (split_symbols, implicit_multiplication,)
    w = Symbol('w', real=True)
    y = Symbol('y')
    assert parse_expr('yx', local_dict={'x':w}, transformations=t) == y*w

