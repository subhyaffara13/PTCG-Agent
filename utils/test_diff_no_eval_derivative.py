
def test_diff_no_eval_derivative():
    class My(Expr):
        def __new__(cls, x):
            return Expr.__new__(cls, x)

    # My doesn't have its own _eval_derivative method
    assert My(x).diff(x).func is Derivative
    assert My(x).diff(x, 3).func is Derivative
    assert re(x).diff(x, 2) == Derivative(re(x), (x, 2))  # issue 15518
    assert diff(NDimArray([re(x), im(x)]), (x, 2)) == NDimArray(
        [Derivative(re(x), (x, 2)), Derivative(im(x), (x, 2))])
    # it doesn't have y so it shouldn't need a method for this case
    assert My(x).diff(y) == 0

