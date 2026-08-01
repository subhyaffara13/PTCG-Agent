
def test_issue_6632_evalf():
    add = (-100000*sqrt(2500000001) + 5000000001)
    assert add.n() == 9.999999998e-11
    assert (add*add).n() == 9.999999996e-21

