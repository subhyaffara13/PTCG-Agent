
def test_sympy__codegen__abstract_nodes__List():
    from sympy.codegen.abstract_nodes import List
    assert _test_args(List(1, 2, 3))

