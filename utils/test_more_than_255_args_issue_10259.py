
def test_more_than_255_args_issue_10259():
    from sympy.core.add import Add
    from sympy.core.mul import Mul
    for op in (Add, Mul):
        expr = op(*symbols('x:256'))
        assert eval(srepr(expr)) == expr

