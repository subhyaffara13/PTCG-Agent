
def test_minpoly_op_algebraic_element_not_impl():
    raises(NotImplementedError,
           lambda: _minpoly_op_algebraic_element(Pow, sqrt(2), sqrt(3), x, QQ))

