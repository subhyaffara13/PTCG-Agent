
def test_issue_25043():
    c = symbols("c")
    x = symbols("x0", real=True)
    cse_expr = cse(c*x**2 + c*(x**4 - x**2))[-1][-1]
    free = cse_expr.free_symbols
    assert len(free) == len({i.name for i in free})

