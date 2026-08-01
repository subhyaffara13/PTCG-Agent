
def test_issue_2941():
    def _check():
        for f, g in cartes(*[(Line, Ray, Segment)] * 2):
            l1 = f(a, b)
            l2 = g(c, d)
            assert l1.intersection(l2) == l2.intersection(l1)
    # intersect at end point
    c, d = (-2, -2), (-2, 0)
    a, b = (0, 0), (1, 1)
    _check()
    # midline intersection
    c, d = (-2, -3), (-2, 0)
    _check()

