
def test_issue_4136():
    assert cosh(asinh(Integer(3)/2)) == sqrt(Integer(13)/4)

