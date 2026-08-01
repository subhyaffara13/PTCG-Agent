
def test_issue_4373():
    x = Symbol("x")
    assert abs(trigsimp(2.0*sin(x)**2 + 2.0*cos(x)**2) - 2.0) < 1e-10

