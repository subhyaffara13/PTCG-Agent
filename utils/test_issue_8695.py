
def test_issue_8695():
    p = (x**2 + 1) * (x - 1)**2 * (x - 2)**3 * (x - 3)**3
    result = (1, [(x**2 + 1, 1), (x - 1, 2), (x**2 - 5*x + 6, 3)])
    assert sqf_list(p) == result

