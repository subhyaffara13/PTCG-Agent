
def test_issue_27284():
    if not numpy:
        skip("numpy not installed.")

    assert Float(numpy.float32(float('inf'))) == S.Infinity
    assert Float(numpy.float32(float('-inf'))) == S.NegativeInfinity

