
def test_issue_17638():

    assert solve(((2-exp(2*x))*exp(x))/(exp(2*x)+2)**2 > 0, x) == (-oo < x) & (x < log(2)/2)
    assert solve(((2-exp(2*x)+2)*exp(x+2))/(exp(x)+2)**2 > 0, x) == (-oo < x) & (x < log(4)/2)
    assert solve((exp(x)+2+x**2)*exp(2*x+2)/(exp(x)+2)**2 > 0, x) == (-oo < x) & (x < oo)

