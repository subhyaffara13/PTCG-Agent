
def test_pytype_rvalue_cast():
    """Make sure that cast from pytype rvalue to other pytype works"""

    value = m.get_pytype_rvalue_castissue(1.0)
    assert value == 1

