
def test_hard_match():
    from sympy.functions.elementary.trigonometric import (cos, sin)
    expr = sin(x) + cos(x)**2
    p, q = map(Symbol, 'pq')
    pattern = sin(p) + cos(p)**2
    assert list(unify(expr, pattern, {}, (p, q))) == [{p: x}]

