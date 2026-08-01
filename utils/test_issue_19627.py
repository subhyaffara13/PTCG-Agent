
def test_issue_19627():
    # if you use force the user must verify
    assert powdenest(sqrt(sin(x)**2), force=True) == sin(x)
    assert powdenest((x**(S.Half/y))**(2*y), force=True) == x
    from sympy.core.function import expand_power_base
    e = 1 - a
    expr = (exp(z/e)*x**(b/e)*y**((1 - b)/e))**e
    assert powdenest(expand_power_base(expr, force=True), force=True
        ) == x**b*y**(1 - b)*exp(z)

