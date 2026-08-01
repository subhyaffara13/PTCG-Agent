
def test_ignore_assumptions():
    # make sure assumptions are ignored
    xpos = symbols('x', positive=True)
    x = symbols('x')
    assert solveset_complex(xpos**2 - 4, xpos
        ) == solveset_complex(x**2 - 4, x)

