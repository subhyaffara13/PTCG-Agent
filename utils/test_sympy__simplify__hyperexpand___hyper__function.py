
def test_sympy__simplify__hyperexpand__Hyper_Function():
    from sympy.simplify.hyperexpand import Hyper_Function
    assert _test_args(Hyper_Function([2], [1]))

