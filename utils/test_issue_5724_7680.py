
def test_issue_5724_7680():
    assert I not in S.Reals  # issue 7680
    assert Interval(-oo, oo).contains(I) is S.false

