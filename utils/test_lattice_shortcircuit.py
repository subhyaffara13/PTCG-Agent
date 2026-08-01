
def test_lattice_shortcircuit():
    raises(SympifyError, lambda: join(object))
    assert join(0, object) == 0

