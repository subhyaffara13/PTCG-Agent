
def test_nested_throws(capture):
    """Tests nested (e.g. C++ -> Python -> C++) exception handling"""

    def throw_myex():
        raise m.MyException("nested error")

    def throw_myex5():
        raise m.MyException5("nested error 5")

    # In the comments below, the exception is caught in the first step, thrown in the last step

    # C++ -> Python
    with capture:
        m.try_catch(m.MyException5, throw_myex5)
    assert str(capture).startswith("MyException5: nested error 5")

    # Python -> C++ -> Python
    with pytest.raises(m.MyException) as excinfo:
        m.try_catch(m.MyException5, throw_myex)
    assert str(excinfo.value) == "nested error"

    def pycatch(exctype, f, *args):  # noqa: ARG001
        try:
            f(*args)
        except m.MyException as e:
            print(e)

    # C++ -> Python -> C++ -> Python
    with capture:
        m.try_catch(
            m.MyException5,
            pycatch,
            m.MyException,
            m.try_catch,
            m.MyException,
            throw_myex5,
        )
    assert str(capture).startswith("MyException5: nested error 5")

    # C++ -> Python -> C++
    with capture:
        m.try_catch(m.MyException, pycatch, m.MyException5, m.throws4)
    assert capture == "this error is rethrown"

    # Python -> C++ -> Python -> C++
    with pytest.raises(m.MyException5) as excinfo:
        m.try_catch(m.MyException, pycatch, m.MyException, m.throws5)
    assert str(excinfo.value) == "this is a helper-defined translated exception"

