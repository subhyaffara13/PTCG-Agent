
def test_doitdoit():
    done = Derivative(f(x, g(x)), x, g(x)).doit()
    assert done == done.doit()

