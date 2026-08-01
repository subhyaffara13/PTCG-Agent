
def test_choose_pref_attach():
    """Add test coverage for the empty `degs` branch in `choose_pref_attach`."""
    assert choose_pref_attach([], seed=42) is None

