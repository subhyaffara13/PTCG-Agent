
def test_global():
    """Test for global assumptions"""
    global_assumptions.add(x > 0)
    assert (x > 0) in global_assumptions
    global_assumptions.remove(x > 0)
    assert not (x > 0) in global_assumptions
    # same with multiple of assumptions
    global_assumptions.add(x > 0, y > 0)
    assert (x > 0) in global_assumptions
    assert (y > 0) in global_assumptions
    global_assumptions.clear()
    assert not (x > 0) in global_assumptions
    assert not (y > 0) in global_assumptions


def test_global():
    """Test ask with global assumptions"""
    assert ask(Q.integer(x)) is None
    global_assumptions.add(Q.integer(x))
    assert ask(Q.integer(x)) is True
    global_assumptions.clear()
    assert ask(Q.integer(x)) is None

