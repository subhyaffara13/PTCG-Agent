
def test_issue_9173():
    p0,p1,p2,p3,b0,b1,b2=symbols('p0 p1 p2 p3 b0 b1 b2')
    Q=(p0+(p1+(p2+p3/y)/y)/y)/(1+((p3/(b0*y)+(b0*p2-b1*p3)/b0**2)/y+\
       (b0**2*p1-b0*b1*p2-p3*(b0*b2-b1**2))/b0**3)/y)

    series = Q.series(y,n=3)

    assert series == y*(b0*p2/p3+b0*(-p2/p3+b1/b0))+y**2*(b0*p1/p3+b0*p2*\
            (-p2/p3+b1/b0)/p3+b0*(-p1/p3+(p2/p3-b1/b0)**2+b1*p2/(b0*p3)+\
            b2/b0-b1**2/b0**2))+b0+O(y**3)
    assert series.simplify() == b2*y**2 + b1*y + b0 + O(y**3)

