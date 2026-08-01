
def test_issue_21661():
    out = limit((x**(x + 1) * (log(x) + 1) + 1) / x, x, 11)
    assert out == S(3138428376722)/11 + 285311670611*log(11)

