
def test_issue_25983():
    assert(reduce_inequalities(pi/Abs(x) <= 1) == ((pi <= x) & (x < oo)) | ((-oo < x) & (x <= -pi)))

