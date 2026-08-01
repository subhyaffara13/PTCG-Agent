
def test_Attribute():
    noexcept = Attribute('noexcept')
    assert noexcept == Attribute('noexcept')
    alignas16 = Attribute('alignas', [16])
    alignas32 = Attribute('alignas', [32])
    assert alignas16 != alignas32
    assert alignas16.func(*alignas16.args) == alignas16

