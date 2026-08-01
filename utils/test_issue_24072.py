
def test_issue_24072():
    assert Piecewise((1, x > 1), (2, x <= 1), (3, x <= 1)
        ) == Piecewise((1, x > 1), (2, True))

