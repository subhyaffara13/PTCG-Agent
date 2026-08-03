from typing import Tuple

def test_issue_15353():
    a, x = symbols('a x')
    # Obtained from nonlinsolve([(sin(a*x)),cos(a*x)],[x,a])
    sol = ConditionSet(
        Tuple(x, a), Eq(sin(a*x), 0) & Eq(cos(a*x), 0), S.Complexes**2)
    assert latex(sol) == \
        r'\left\{\left( x, \  a\right)\; \middle|\; \left( x, \  a\right) \in ' \
        r'\mathbb{C}^{2} \wedge \sin{\left(a x \right)} = 0 \wedge ' \
        r'\cos{\left(a x \right)} = 0 \right\}'

