
def test_diamond_inheritance():
    """Tests that diamond inheritance works as expected (issue #959)"""

    # Issue #959: this shouldn't segfault:
    d = m.D()

    # Make sure all the various distinct pointers are all recognized as registered instances:
    assert d is d.c0()
    assert d is d.c1()
    assert d is d.b()
    assert d is d.c0().b()
    assert d is d.c1().b()
    assert d is d.c0().c1().b().c0().b()

