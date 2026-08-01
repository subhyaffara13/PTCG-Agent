
def test_issue_13835():
    a = symbols('a')
    M = lambda n: Matrix([[i + a*j for i in range(n)]
                          for j in range(n)])
    assert M(5).det() == 0
    assert M(6).det() == 0
    assert M(7).det() == 0

