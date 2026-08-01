
def test_issue_18628():
    eq1 = x**2 - 15*x + y**2 - 8*y
    sol = diophantine(eq1)
    assert sol == {(15, 0), (15, 8), (-1, 4), (0, 0), (0, 8), (16, 4)}
    eq2 = 2*x**2 - 9*x + 4*y**2 - 8*y + 14
    sol = diophantine(eq2)
    assert sol == {(2, 1)}

