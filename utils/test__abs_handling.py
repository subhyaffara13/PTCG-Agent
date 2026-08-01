
def test_Abs_handling():
    x = symbols('x', real=True)
    assert solve(abs(x/y), x) == [0]

