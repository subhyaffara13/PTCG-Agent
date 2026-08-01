
def test_M26():
    # TODO: Replace solve with solveset, as of now test fails for solveset
    assert solve(sqrt(log(x)) - log(sqrt(x))) == [1, exp(4)]

