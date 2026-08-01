
def test_U8():
    x, y = symbols('x y', real=True)
    eq = cos(x*y) + x
    #  If SymPy had implicit_diff() function this hack could be avoided
    # TODO: Replace solve with solveset, current test fails for solveset
    assert idiff(y - eq, y, x) == (-y*sin(x*y) + 1)/(x*sin(x*y) + 1)

