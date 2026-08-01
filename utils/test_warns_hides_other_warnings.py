
def test_warns_hides_other_warnings():
    with raises(RuntimeWarning):
        with warns(UserWarning):
            warnings.warn('this is the warning message', UserWarning)
            warnings.warn('this is the other message', RuntimeWarning)

