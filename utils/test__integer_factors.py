
def test_Integer_factors():
    def F(i):
        return Integer(i).factors()

    assert F(1) == {}
    assert F(2) == {2: 1}
    assert F(3) == {3: 1}
    assert F(4) == {2: 2}
    assert F(5) == {5: 1}
    assert F(6) == {2: 1, 3: 1}
    assert F(7) == {7: 1}
    assert F(8) == {2: 3}
    assert F(9) == {3: 2}
    assert F(10) == {2: 1, 5: 1}
    assert F(11) == {11: 1}
    assert F(12) == {2: 2, 3: 1}
    assert F(13) == {13: 1}
    assert F(14) == {2: 1, 7: 1}
    assert F(15) == {3: 1, 5: 1}
    assert F(16) == {2: 4}
    assert F(17) == {17: 1}
    assert F(18) == {2: 1, 3: 2}
    assert F(19) == {19: 1}
    assert F(20) == {2: 2, 5: 1}
    assert F(21) == {3: 1, 7: 1}
    assert F(22) == {2: 1, 11: 1}
    assert F(23) == {23: 1}
    assert F(24) == {2: 3, 3: 1}
    assert F(25) == {5: 2}
    assert F(26) == {2: 1, 13: 1}
    assert F(27) == {3: 3}
    assert F(28) == {2: 2, 7: 1}
    assert F(29) == {29: 1}
    assert F(30) == {2: 1, 3: 1, 5: 1}
    assert F(31) == {31: 1}
    assert F(32) == {2: 5}
    assert F(33) == {3: 1, 11: 1}
    assert F(34) == {2: 1, 17: 1}
    assert F(35) == {5: 1, 7: 1}
    assert F(36) == {2: 2, 3: 2}
    assert F(37) == {37: 1}
    assert F(38) == {2: 1, 19: 1}
    assert F(39) == {3: 1, 13: 1}
    assert F(40) == {2: 3, 5: 1}
    assert F(41) == {41: 1}
    assert F(42) == {2: 1, 3: 1, 7: 1}
    assert F(43) == {43: 1}
    assert F(44) == {2: 2, 11: 1}
    assert F(45) == {3: 2, 5: 1}
    assert F(46) == {2: 1, 23: 1}
    assert F(47) == {47: 1}
    assert F(48) == {2: 4, 3: 1}
    assert F(49) == {7: 2}
    assert F(50) == {2: 1, 5: 2}
    assert F(51) == {3: 1, 17: 1}

