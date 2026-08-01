
def test_shifted_sum():
    from sympy.simplify.simplify import simplify
    assert simplify(hyperexpand(z**4*hyper([2], [3, S('3/2')], -z**2))) \
        == z*sin(2*z) + (-z**2 + S.Half)*cos(2*z) - S.Half

