
def test_minpoly_issue_7113():
    # see discussion in https://github.com/sympy/sympy/pull/2234
    from sympy.simplify.simplify import nsimplify
    r = nsimplify(pi, tolerance=0.000000001)
    mp = minimal_polynomial(r, x)
    assert mp == 1768292677839237920489538677417507171630859375*x**109 - \
    2734577732179183863586489182929671773182898498218854181690460140337930774573792597743853652058046464

