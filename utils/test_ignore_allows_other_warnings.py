
def test_ignore_allows_other_warnings():
    with warnings.catch_warnings(record=True) as w:
        # This is needed when pytest is run as -Werror
        # the setting is reverted at the end of the catch_Warnings block.
        warnings.simplefilter("always")
        with ignore_warnings(UserWarning):
            warnings.warn('this is the warning message', UserWarning)
            warnings.warn('this is the other message', RuntimeWarning)
        assert len(w) == 1
        assert isinstance(w[0].message, RuntimeWarning)
        assert str(w[0].message) == 'this is the other message'

