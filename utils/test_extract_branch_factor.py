
def test_extract_branch_factor():
    assert exp_polar(2.0*I*pi).extract_branch_factor() == (1, 1)

