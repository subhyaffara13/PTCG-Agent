
def test_callbacks():
    from functools import partial

    def func1():
        return "func1"

    def func2(a, b, c, d):
        return "func2", a, b, c, d

    def func3(a):
        return f"func3({a})"

    assert m.test_callback1(func1) == "func1"
    assert m.test_callback2(func2) == ("func2", "Hello", "x", True, 5)
    assert m.test_callback1(partial(func2, 1, 2, 3, 4)) == ("func2", 1, 2, 3, 4)
    assert m.test_callback1(partial(func3, "partial")) == "func3(partial)"
    assert m.test_callback3(lambda i: i + 1) == "func(43) = 44"

    f = m.test_callback4()
    assert f(43) == 44
    f = m.test_callback5()
    assert f(number=43) == 44


def test_callbacks():
    def check(caller, func, user_data):
        caller = CALLERS[caller]
        func = FUNCS[func]()
        user_data = USER_DATAS[user_data]()

        if func is callback_python:
            def func2(x):
                return func(x, 2.0)
        else:
            func2 = LowLevelCallable(func, user_data)
            func = LowLevelCallable(func)

        # Test basic call
        assert_equal(caller(func, 1.0), 2.0)

        # Test 'bad' value resulting to an error
        assert_raises(ValueError, caller, func, ERROR_VALUE)

        # Test passing in user_data
        assert_equal(caller(func2, 1.0), 3.0)

    for caller in sorted(CALLERS.keys()):
        for func in sorted(FUNCS.keys()):
            for user_data in sorted(USER_DATAS.keys()):
                check(caller, func, user_data)


def test_callbacks():
    def func(artist):
        func.counter += 1

    func.counter = 0

    art = martist.Artist()
    oid = art.add_callback(func)
    assert func.counter == 0
    art.pchanged()  # must call the callback
    assert func.counter == 1
    art.set_zorder(10)  # setting a property must also call the callback
    assert func.counter == 2
    art.remove_callback(oid)
    art.pchanged()  # must not call the callback anymore
    assert func.counter == 2

