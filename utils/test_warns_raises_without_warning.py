
def test_warns_raises_without_warning():
    with raises(Failed):
        with warns(UserWarning):
            pass

