
def test_M36():
    # TODO: Replace solve with solveset, as of now
    # solveset doesn't supports solving for function
    # assert solve(f**2 + f - 2, x) == [Eq(f(x), 1), Eq(f(x), -2)]
    assert solveset(f(x)**2 + f(x) - 2, f(x)) == FiniteSet(-2, 1)

