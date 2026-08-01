
def test_Domain_get_ring():
    assert ZZ.has_assoc_Ring is True
    assert QQ.has_assoc_Ring is True
    assert ZZ[x].has_assoc_Ring is True
    assert QQ[x].has_assoc_Ring is True
    assert ZZ[x, y].has_assoc_Ring is True
    assert QQ[x, y].has_assoc_Ring is True
    assert ZZ.frac_field(x).has_assoc_Ring is True
    assert QQ.frac_field(x).has_assoc_Ring is True
    assert ZZ.frac_field(x, y).has_assoc_Ring is True
    assert QQ.frac_field(x, y).has_assoc_Ring is True

    assert EX.has_assoc_Ring is False
    assert RR.has_assoc_Ring is False
    assert ALG.has_assoc_Ring is False

    assert ZZ.get_ring() == ZZ
    assert QQ.get_ring() == ZZ
    assert ZZ[x].get_ring() == ZZ[x]
    assert QQ[x].get_ring() == QQ[x]
    assert ZZ[x, y].get_ring() == ZZ[x, y]
    assert QQ[x, y].get_ring() == QQ[x, y]
    assert ZZ.frac_field(x).get_ring() == ZZ[x]
    assert QQ.frac_field(x).get_ring() == QQ[x]
    assert ZZ.frac_field(x, y).get_ring() == ZZ[x, y]
    assert QQ.frac_field(x, y).get_ring() == QQ[x, y]

    assert EX.get_ring() == EX

    assert RR.get_ring() == RR
    # XXX: This should also be like RR
    raises(DomainError, lambda: ALG.get_ring())

