
def test_issue_2840_8155():
    # with parameter-free solutions (i.e. no `n`), we want to avoid
    # excessive periodic solutions
    assert solve(sin(3*x) + sin(6*x)) == [0, -2*pi/9, 2*pi/9]
    assert solve(sin(300*x) + sin(600*x)) == [0, -pi/450, pi/450]
    assert solve(2*sin(x) - 2*sin(2*x)) == [0, -pi/3, pi/3]

