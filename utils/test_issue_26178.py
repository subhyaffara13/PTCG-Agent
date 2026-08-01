
def test_issue_26178():
    R, x, y, z = ring(['x', 'y', 'z'], QQ)
    assert (x**2 - 2*y**2 + 1).sqf_list() == (MPQ(1,1), [(x**2 - 2*y**2 + 1, 1)])
    assert (x**2 - 2*z**2 + 1).sqf_list() == (MPQ(1,1), [(x**2 - 2*z**2 + 1, 1)])
    assert (y**2 - 2*z**2 + 1).sqf_list() == (MPQ(1,1), [(y**2 - 2*z**2 + 1, 1)])

