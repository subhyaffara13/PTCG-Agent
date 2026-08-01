
def test_issue_19869():
    assert (maximum(sqrt(3)*(x - 1)/(3*sqrt(x**2 + 1)), x)
        ) == sqrt(3)/3

