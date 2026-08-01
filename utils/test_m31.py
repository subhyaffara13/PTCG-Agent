
def test_M31():
    # TODO: Replace solve with solveset, as of now
    # solveset doesn't supports assumptions
    # assert solve(1 - abs(x) - max(-x - 2, x - 2),x, assume=Q.real(x)) == [-3/2, 3/2]
    assert solveset_real(1 - abs(x) - Max(-x - 2, x - 2), x) == FiniteSet(R(-3, 2), R(3, 2))

