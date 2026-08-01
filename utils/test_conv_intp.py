
def test_conv_intp(install_temp):
    import checks

    class myint:
        def __int__(self):
            return 3

    # These conversion passes via `__int__`, not `__index__`:
    assert checks.conv_intp(3.) == 3
    assert checks.conv_intp(myint()) == 3

