
def test_ignore_ignores_warning():
    with warnings.catch_warnings(record=True) as w:
        with ignore_warnings(UserWarning):
            warnings.warn('this is the warning message')
        assert len(w) == 0

