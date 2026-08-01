
def test_issue_refine_9384():
    assert refine(Piecewise((1, x < 0), (0, True)), Q.positive(x)) == 0
    assert refine(Piecewise((1, x < 0), (0, True)), Q.negative(x)) == 1
    assert refine(Piecewise((1, x > 0), (0, True)), Q.positive(x)) == 1
    assert refine(Piecewise((1, x > 0), (0, True)), Q.negative(x)) == 0

