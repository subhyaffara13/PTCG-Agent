
def test_M25():
    a, b, c, d = symbols(':d', positive=True)
    x = symbols('x')
    # TODO: Replace solve with solveset, as of now test fails for solveset
    assert solve(a*b**x - c*d**x, x)[0].expand() == (log(c/a)/log(b/d)).expand()

