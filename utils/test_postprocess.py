
def test_postprocess():
    eq = (x + 1 + exp((x + 1)/(y + 1)) + cos(y + 1))
    assert cse([eq, Eq(x, z + 1), z - 2, (z + 1)*(x + 1)],
        postprocess=cse_main.cse_separate) == \
        [[(x0, y + 1), (x2, z + 1), (x, x2), (x1, x + 1)],
        [x1 + exp(x1/x0) + cos(x0), z - 2, x1*x2]]

