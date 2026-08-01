
def test_issue_19509():
    a = S(3)/4
    b = S(5)/8
    c = sqrt(5)/8
    d = sqrt(5)/4
    assert solve(1/(x -1)**5 - 1) == [2,
        -d + a - sqrt(-b + c),
        -d + a + sqrt(-b + c),
        d + a - sqrt(-b - c),
        d + a + sqrt(-b - c)]

