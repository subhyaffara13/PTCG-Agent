
def test_M19():
    # TODO: Replace solve with solveset, as of now test fails for solveset
    assert solve((x - 2)/x**R(1, 3), x) == [2]

