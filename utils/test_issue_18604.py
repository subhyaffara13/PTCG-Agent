
def test_issue_18604():
    m = symbols("m")
    assert Idx("i", m).name == 'i'
    assert Idx("i", m).lower == 0
    assert Idx("i", m).upper == m - 1
    m = symbols("m", real=False)
    raises(TypeError, lambda: Idx("i", m))

