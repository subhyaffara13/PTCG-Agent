
def test_unregistered_base_implementations():
    a = m.RegisteredDerived()
    a.do_nothing()
    assert a.rw_value == 42
    assert a.ro_value == 1.25
    a.rw_value += 5
    assert a.sum() == 48.25
    a.increase_value()
    assert a.rw_value == 48
    assert a.ro_value == 1.5
    assert a.sum() == 49.5
    assert a.rw_value_prop == 48
    a.rw_value_prop += 1
    assert a.rw_value_prop == 49
    a.increase_value()
    assert a.ro_value_prop == 1.75

