
def test_rcollect():
    assert rcollect((x**2*y + x*y + x + y)/(x + y), y) == \
        (x + y*(1 + x + x**2))/(x + y)
    assert rcollect(sqrt(-((x + 1)*(y + 1))), z) == sqrt(-((x + 1)*(y + 1)))


def test_rcollect():
    assert rcollect(A*B - B*A, A) == A*B - B*A
    assert rcollect(A*B - B*A, B) == A*B - B*A
    assert rcollect(A*B - B*A, x) == A*B - B*A

