
def test_issue_14240():
    assert piecewise_fold(
        Piecewise((1, a), (2, b), (4, True)) +
        Piecewise((8, a), (16, True))
        ) == Piecewise((9, a), (18, b), (20, True))
    assert piecewise_fold(
        Piecewise((2, a), (3, b), (5, True)) *
        Piecewise((7, a), (11, True))
        ) == Piecewise((14, a), (33, b), (55, True))
    # these will hang if naive folding is used
    assert piecewise_fold(Add(*[
        Piecewise((i, a), (0, True)) for i in range(40)])
        ) == Piecewise((780, a), (0, True))
    assert piecewise_fold(Mul(*[
        Piecewise((i, a), (0, True)) for i in range(1, 41)])
        ) == Piecewise((factorial(40), a), (0, True))

