
def test_holder_with_addressof_operator():
    # this test must not throw exception from c++
    a = m.TypeForHolderWithAddressOf.make()
    a.print_object_1()
    a.print_object_2()
    a.print_object_3()
    a.print_object_4()

    stats = ConstructorStats.get(m.TypeForHolderWithAddressOf)
    assert stats.alive() == 1

    np = m.TypeForHolderWithAddressOf.make()
    assert stats.alive() == 2
    del a
    assert stats.alive() == 1
    del np
    assert stats.alive() == 0

    b = m.TypeForHolderWithAddressOf.make()
    c = b
    assert b.get() is c.get()
    assert stats.alive() == 1

    del b
    assert stats.alive() == 1

    del c
    assert stats.alive() == 0

