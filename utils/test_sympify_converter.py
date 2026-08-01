
def test_sympify_converter():
    """Tests the resolution order for classes in converter"""
    class a:
        pass
    class b(a):
        pass
    class c(a):
        pass

    converter[a] = lambda x: Integer(1)
    converter[b] = lambda x: Integer(2)

    assert sympify(a()) == Integer(1)
    assert sympify(b()) == Integer(2)
    assert sympify(c()) == Integer(1)

    class MyInteger(Integer):
        pass

    if int in converter:
        int_converter = converter[int]
    else:
        int_converter = None

    try:
        converter[int] = MyInteger
        assert sympify(1) == MyInteger(1)
    finally:
        if int_converter is None:
            del converter[int]
        else:
            converter[int] = int_converter

