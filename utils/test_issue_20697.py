
def test_issue_20697():
    p_0, p_1, p_2, p_3, b_0, b_1, b_2 = symbols('p_0 p_1 p_2 p_3 b_0 b_1 b_2')
    Q = (p_0 + (p_1 + (p_2 + p_3/y)/y)/y)/(1 + ((p_3/(b_0*y) + (b_0*p_2\
        - b_1*p_3)/b_0**2)/y + (b_0**2*p_1 - b_0*b_1*p_2 - p_3*(b_0*b_2\
        - b_1**2))/b_0**3)/y)
    assert Q.series(y, n=3).ratsimp() == b_2*y**2 + b_1*y + b_0 + O(y**3)

