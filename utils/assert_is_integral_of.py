
def assert_is_integral_of(f: Expr, F: Expr):
    assert manualintegrate(f, x) == F
    assert F.diff(x).equals(f)

