
def test_issue_21671():
    assert integrate(1,(z,x**2+y**2,2-x**2-y**2),(y,-sqrt(1-x**2),sqrt(1-x**2)),(x,-1,1)) == pi
    assert integrate(-4*(1 - x**2)**(S(3)/2)/3 + 2*sqrt(1 - x**2)*(2 - 2*x**2), (x, -1, 1)) == pi

