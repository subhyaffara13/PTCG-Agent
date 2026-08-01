
def test_issue_18653():
    x, y, z = symbols("x y z")
    f, g, h = symbols("f g h", cls=Function, args=(x, y))
    f, g, h = f(), g(), h()
    expr2 = f.diff(x)*h.diff(z)
    assert euler(expr2, (f,), (x, y)) == []

