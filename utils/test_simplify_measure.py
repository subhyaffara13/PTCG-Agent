
def test_simplify_measure():
    measure1 = lambda expr: len(str(expr))
    measure2 = lambda expr: -count_ops(expr)
                                       # Return the most complicated result
    expr = (x + 1)/(x + sin(x)**2 + cos(x)**2)
    assert measure1(simplify(expr, measure=measure1)) <= measure1(expr)
    assert measure2(simplify(expr, measure=measure2)) <= measure2(expr)

    expr2 = Eq(sin(x)**2 + cos(x)**2, 1)
    assert measure1(simplify(expr2, measure=measure1)) <= measure1(expr2)
    assert measure2(simplify(expr2, measure=measure2)) <= measure2(expr2)

