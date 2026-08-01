
def test_issue_7426():
    f1 = a % c
    f2 = x % z
    assert f1.equals(f2) is None

