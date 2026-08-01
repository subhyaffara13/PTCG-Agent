
def test_available():
    # Private name should not be listed in available but still usable.
    assert '_classic_test_patch' not in style.available
    assert '_classic_test_patch' in style.library

    with temp_style('_test_', DUMMY_SETTINGS), temp_style('dummy', DUMMY_SETTINGS):
        assert 'dummy' in style.available
        assert 'dummy' in style.library
        assert '_test_' not in style.available
        assert '_test_' in style.library
    assert 'dummy' not in style.available
    assert '_test_' not in style.available

