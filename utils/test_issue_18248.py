
def test_issue_18248():
    assert nonlinsolve([x*y**3-sqrt(2)/3, x*y**6-4/(9*(sqrt(3)))],x,y) == \
            FiniteSet((sqrt(3)/2, sqrt(6)/3), (sqrt(3)/2, -sqrt(6)/6 - sqrt(2)*I/2),
            (sqrt(3)/2, -sqrt(6)/6 + sqrt(2)*I/2))

