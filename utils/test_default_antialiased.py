
def test_default_antialiased():
    patch = Patch()

    patch.set_antialiased(not rcParams['patch.antialiased'])
    assert patch.get_antialiased() == (not rcParams['patch.antialiased'])
    # Check that None resets the state
    patch.set_antialiased(None)
    assert patch.get_antialiased() == rcParams['patch.antialiased']

