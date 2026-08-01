
def test_get_mod_func():
    assert get_mod_func(
        'sympy.core.basic.Basic') == ('sympy.core.basic', 'Basic')

