
def test_ignore_many_warnings():
    with warnings.catch_warnings(record=True) as w:
        # This is needed when pytest is run as -Werror
        # the setting is reverted at the end of the catch_Warnings block.
        warnings.simplefilter("always")
        with ignore_warnings(UserWarning):
            warnings.warn('this is the warning message', UserWarning)
            warnings.warn('this is the other message', RuntimeWarning)
            warnings.warn('this is the warning message', UserWarning)
            warnings.warn('this is the other message', RuntimeWarning)
            warnings.warn('this is the other message', RuntimeWarning)
        assert len(w) == 3
        for wi in w:
            assert isinstance(wi.message, RuntimeWarning)
            assert str(wi.message) == 'this is the other message'

