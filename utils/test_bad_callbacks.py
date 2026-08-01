
def test_bad_callbacks():
    def check(caller, func, user_data):
        caller = CALLERS[caller]
        user_data = USER_DATAS[user_data]()
        func = BAD_FUNCS[func]()

        if func is callback_python:
            def func2(x):
                return func(x, 2.0)
        else:
            func2 = LowLevelCallable(func, user_data)
            func = LowLevelCallable(func)

        # Test that basic call fails
        assert_raises(ValueError, caller, LowLevelCallable(func), 1.0)

        # Test that passing in user_data also fails
        assert_raises(ValueError, caller, func2, 1.0)

        # Test error message
        llfunc = LowLevelCallable(func)
        try:
            caller(llfunc, 1.0)
        except ValueError as err:
            msg = str(err)
            assert_(llfunc.signature in msg, msg)
            assert_('double (double, double, int *, void *)' in msg, msg)

    for caller in sorted(CALLERS.keys()):
        for func in sorted(BAD_FUNCS.keys()):
            for user_data in sorted(USER_DATAS.keys()):
                check(caller, func, user_data)

