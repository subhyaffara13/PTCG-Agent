
def test_super_sub_symmetry(p1, p2, expected):
    assert is_superperiod(p1, p2) is expected
    assert is_subperiod(p2, p1) is expected

