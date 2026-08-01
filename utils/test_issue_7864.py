
def test_issue_7864():
    q, r = div(a, .408248290463863*a)
    assert abs(q - 2.44948974278318) < 1e-14
    assert r == 0

