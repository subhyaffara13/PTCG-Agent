
def test_issue_18505():
    assert ImageSet(Lambda(n, sqrt(pi*n/2 - 1 + pi/2)), S.Integers).contains(0) == \
            Contains(0, ImageSet(Lambda(n, sqrt(pi*n/2 - 1 + pi/2)), S.Integers))

