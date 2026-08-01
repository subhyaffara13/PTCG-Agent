
def test_Domain_is_field():
    assert ZZ.is_Field is False
    assert GF(5).is_Field is True
    assert GF(6).is_Field is False
    assert QQ.is_Field is True
    assert RR.is_Field is True
    assert CC.is_Field is True
    assert EX.is_Field is True
    assert ALG.is_Field is True
    assert QQ[x].is_Field is False
    assert ZZ.frac_field(x).is_Field is True

