
def test_Float_gcd_lcm_cofactors():
    assert Float(2.0).gcd(Integer(4)) == Float(1.0)
    assert Float(2.0).lcm(Integer(4)) == Float(8.0)
    assert Float(2.0).cofactors(Integer(4)) == (Float(1.0), Float(2.0), Float(4.0))

    assert Float(2.0).gcd(S.Half) == Float(1.0)
    assert Float(2.0).lcm(S.Half) == Float(1.0)
    assert Float(2.0).cofactors(S.Half) == \
        (Float(1.0), Float(2.0), Float(0.5))

