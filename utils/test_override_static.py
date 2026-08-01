
def test_override_static():
    """#511: problem with inheritance + overwritten def_static"""
    b = m.MyBase.make()
    d1 = m.MyDerived.make2()
    d2 = m.MyDerived.make()

    assert isinstance(b, m.MyBase)
    assert isinstance(d1, m.MyDerived)
    assert isinstance(d2, m.MyDerived)

