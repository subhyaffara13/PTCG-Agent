
def test_M30():
    # TODO: Replace solve with solveset, as of now
    # solveset doesn't supports assumptions
    # assert solve(abs(2*x + 5) - abs(x - 2),x, assume=Q.real(x)) == [-1, -7]
    assert solveset_real(abs(2*x + 5) - abs(x - 2), x) == FiniteSet(-1, -7)

