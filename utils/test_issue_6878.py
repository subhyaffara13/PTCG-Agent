
def test_issue_6878():
    n = symbols('n', integer=True)
    assert combsimp(RisingFactorial(-10, n)) == 3628800*(-1)**n/factorial(10 - n)

