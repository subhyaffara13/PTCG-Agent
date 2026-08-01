
def test_warns_many_warnings():
    with warns(UserWarning):
        warnings.warn('this is the warning message', UserWarning)
        warnings.warn('this is the other warning message', UserWarning)

