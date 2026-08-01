
def test_issue_2975():
    w = Symbol('w')
    C = Symbol('C')
    y = Symbol('y')
    assert integrate(1/(y**2+C)**(S(3)/2), (y, -w/2, w/2)) == w/(C**(S(3)/2)*sqrt(1 + w**2/(4*C)))

