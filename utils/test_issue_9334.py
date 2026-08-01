
def test_issue_9334():
    if not numexpr:
        skip("numexpr not installed.")
    if not numpy:
        skip("numpy not installed.")
    expr = S('b*a - sqrt(a**2)')
    a, b = sorted(expr.free_symbols, key=lambda s: s.name)
    func_numexpr = lambdify((a,b), expr, modules=[numexpr], dummify=False)
    foo, bar = numpy.random.random((2, 4))
    func_numexpr(foo, bar)

