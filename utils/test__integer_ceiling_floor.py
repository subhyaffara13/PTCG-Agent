
def test_Integer_ceiling_floor():
    a = Integer(4)

    assert a.floor() == a
    assert a.ceiling() == a

