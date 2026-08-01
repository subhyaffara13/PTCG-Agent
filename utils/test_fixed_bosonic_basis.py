
def test_fixed_bosonic_basis():
    b = FixedBosonicBasis(2, 2)
    # assert b == [FockState((2, 0)), FockState((1, 1)), FockState((0, 2))]
    state = b.state(1)
    assert state == FockStateBosonKet((1, 1))
    assert b.index(state) == 1
    assert b.state(1) == b[1]
    assert len(b) == 3
    assert str(b) == '[FockState((2, 0)), FockState((1, 1)), FockState((0, 2))]'
    assert repr(b) == '[FockState((2, 0)), FockState((1, 1)), FockState((0, 2))]'
    assert srepr(b) == '[FockState((2, 0)), FockState((1, 1)), FockState((0, 2))]'

