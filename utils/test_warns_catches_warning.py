
def test_warns_catches_warning():
    with warnings.catch_warnings(record=True) as w:
        with warns(UserWarning):
            warnings.warn('this is the warning message')
        assert len(w) == 0

