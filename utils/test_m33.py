
def test_M33():
    # TODO: Replace solve with solveset, as of now
    # solveset doesn't supports assumptions

    # Second answer can be written in another form. The second answer is the root of x**3 + 9*x**2 - 18 = 0 in the interval (-2, -1).
    assert solveset_real(Max(2 - x**2, x) - x**3/9, x) == FiniteSet(-3, -1.554894, 3)

