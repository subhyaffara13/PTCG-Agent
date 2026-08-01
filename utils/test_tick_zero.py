
def test_tick_zero(cls1, cls2):
    assert cls1(0) == cls2(0)
    assert cls1(0) + cls2(0) == cls1(0)

    if cls1 is not Nano:
        assert cls1(2) + cls2(0) == cls1(2)

    if cls1 is Nano:
        assert cls1(2) + Nano(0) == cls1(2)

