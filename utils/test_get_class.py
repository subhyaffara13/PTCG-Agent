
def test_get_class():
    _basic = get_class('sympy.core.basic.Basic')
    assert _basic.__name__ == 'Basic'

