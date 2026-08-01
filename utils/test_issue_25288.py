
def test_issue_25288():
    syms = numbered_symbols(cls=Dummy)
    ok = lambdify(x, [x**2, sin(x**2)], cse=lambda e: cse(e, symbols=syms))(2)
    assert ok

