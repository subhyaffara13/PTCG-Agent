
def test_evalf_issue_3273():
    assert Sum(0, (k, 1, oo)).evalf() == 0

