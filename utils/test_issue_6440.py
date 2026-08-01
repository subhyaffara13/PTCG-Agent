
def test_issue_6440():
    assert powsimp(16*2**a*8**b) == 2**(a + 3*b + 4)

