
def test_issue_4124():
    from sympy.core.numbers import oo
    assert expand_complex(I*oo) == oo*I

