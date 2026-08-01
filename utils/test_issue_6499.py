
def test_issue_6499():
    assert residue(1/(exp(z) - 1), z, 0) == 1

