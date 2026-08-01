
def test_issue_8943():
    assert diophantine(
        3*(x**2 + y**2 + z**2) - 14*(x*y + y*z + z*x)) == \
           {(0, 0, 0)}

