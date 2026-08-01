
def test_issue_24609_xfail():
    #
    # This returns 5 solutions when it should be 1 (with x positive).
    # Simplification reveals all solutions to be equivalent. It is expected
    # that solve without simplify=True returns duplicate solutions in some
    # cases but the core of this equation is a simple quadratic that can easily
    # be solved without introducing any redundant solutions:
    #
    #     >>> print(factor_terms(eq.as_numer_denom()[0]))
    #     2**(2/3)*pi**(2/3)*D_c*V**(2/3)*x**(7/3)*(231361*x**2 - 20000*pi**2)
    #
    eq, expected, x = _make_example_24609()
    assert len(solve(eq, x)) == [expected]

