
def test_M32():
    # TODO: Replace solve with solveset, as of now
    # solveset doesn't supports assumptions
    assert solveset_real(Max(2 - x**2, x)- Max(-x, (x**3)/9), x) == FiniteSet(-1, 3)

