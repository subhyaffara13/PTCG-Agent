
def test_reciprocal_functions():
    assert sec(3).ae(-1.01010866590799375)
    assert csc(3).ae(7.08616739573718592)
    assert cot(3).ae(-7.01525255143453347)
    assert sech(3).ae(0.0993279274194332078)
    assert csch(3).ae(0.0998215696688227329)
    assert coth(3).ae(1.00496982331368917)
    assert asec(3).ae(1.23095941734077468)
    assert acsc(3).ae(0.339836909454121937)
    assert acot(3).ae(0.321750554396642193)
    assert asech(0.5).ae(1.31695789692481671)
    assert acsch(3).ae(0.327450150237258443)
    assert acoth(3).ae(0.346573590279972655)
    assert acot(0).ae(1.5707963267948966192)
    assert acoth(0).ae(1.5707963267948966192j)

