
def test__simple_dens():
    assert _simple_dens(1/x**0, [x]) == set()
    assert _simple_dens(1/x**y, [x]) == {x**y}
    assert _simple_dens(1/root(x, 3), [x]) == {x}

