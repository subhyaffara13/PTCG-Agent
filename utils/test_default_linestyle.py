
def test_default_linestyle():
    patch = Patch()
    patch.set_linestyle('--')
    patch.set_linestyle(None)
    assert patch.get_linestyle() == 'solid'

