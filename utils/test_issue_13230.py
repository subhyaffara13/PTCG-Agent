
def test_issue_13230():
    c1 = Circle(Point2D(3, sqrt(5)), 5)
    c2 = Circle(Point2D(4, sqrt(7)), 6)
    assert intersection(c1, c2) == [Point2D(-1 + (-sqrt(7) + sqrt(5))*(-2*sqrt(7)/29
    + 9*sqrt(5)/29 + sqrt(196*sqrt(35) + 1941)/29), -2*sqrt(7)/29 + 9*sqrt(5)/29
    + sqrt(196*sqrt(35) + 1941)/29), Point2D(-1 + (-sqrt(7) + sqrt(5))*(-sqrt(196*sqrt(35)
    + 1941)/29 - 2*sqrt(7)/29 + 9*sqrt(5)/29), -sqrt(196*sqrt(35) + 1941)/29 - 2*sqrt(7)/29 + 9*sqrt(5)/29)]

