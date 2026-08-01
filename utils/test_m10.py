
def test_M10():
    # TODO: Replace solve with solveset when it gives Lambert solution
    assert solve(exp(x) - x, x) == [-LambertW(-1)]

