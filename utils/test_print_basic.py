
def test_print_basic():
    # Issue 15303
    from sympy.core.basic import Basic
    from sympy.core.expr import Expr

    # dummy class for testing printing where the function is not
    # implemented in latex.py
    class UnimplementedExpr(Expr):
        def __new__(cls, e):
            return Basic.__new__(cls, e)

    # dummy function for testing
    def unimplemented_expr(expr):
        return UnimplementedExpr(expr).doit()

    # override class name to use superscript / subscript
    def unimplemented_expr_sup_sub(expr):
        result = UnimplementedExpr(expr)
        result.__class__.__name__ = 'UnimplementedExpr_x^1'
        return result

    assert latex(unimplemented_expr(x)) == r'\operatorname{UnimplementedExpr}\left(x\right)'
    assert latex(unimplemented_expr(x**2)) == \
        r'\operatorname{UnimplementedExpr}\left(x^{2}\right)'
    assert latex(unimplemented_expr_sup_sub(x)) == \
        r'\operatorname{UnimplementedExpr^{1}_{x}}\left(x\right)'


def test_print_basic():
    expr = Basic(S(1), S(2))
    assert mpp.doprint(expr) == \
        '<mrow><mi>basic</mi><mrow><mo>(</mo><mn>1</mn><mo>,</mo><mn>2</mn><mo>)</mo></mrow></mrow>'
    assert mp.doprint(expr) == '<basic><cn>1</cn><cn>2</cn></basic>'

