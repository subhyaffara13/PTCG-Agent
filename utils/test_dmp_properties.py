
def test_DMP_properties():
    assert DMP([[]], ZZ).is_zero is True
    assert DMP([[ZZ(1)]], ZZ).is_zero is False

    assert DMP([[ZZ(1)]], ZZ).is_one is True
    assert DMP([[ZZ(2)]], ZZ).is_one is False

    assert DMP([[ZZ(1)]], ZZ).is_ground is True
    assert DMP([[ZZ(1)], [ZZ(2)], [ZZ(1)]], ZZ).is_ground is False

    assert DMP([[ZZ(1)], [ZZ(2), ZZ(0)], [ZZ(1), ZZ(0)]], ZZ).is_sqf is True
    assert DMP([[ZZ(1)], [ZZ(2), ZZ(0)], [ZZ(1), ZZ(0), ZZ(0)]], ZZ).is_sqf is False

    assert DMP([[ZZ(1), ZZ(2)], [ZZ(3)]], ZZ).is_monic is True
    assert DMP([[ZZ(2), ZZ(2)], [ZZ(3)]], ZZ).is_monic is False

    assert DMP([[ZZ(1), ZZ(2)], [ZZ(3)]], ZZ).is_primitive is True
    assert DMP([[ZZ(2), ZZ(4)], [ZZ(6)]], ZZ).is_primitive is False

