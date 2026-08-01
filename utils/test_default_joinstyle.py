
def test_default_joinstyle():
    patch = Patch()
    assert patch.get_joinstyle() == 'miter'

