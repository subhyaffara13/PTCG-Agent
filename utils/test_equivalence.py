
def test_equivalence():
    a = intervalMembership(True, True)
    b = intervalMembership(True, False)
    assert (a == b) is False
    assert (a != b) is True

    a = intervalMembership(True, False)
    b = intervalMembership(True, False)
    assert (a == b) is True
    assert (a != b) is False

