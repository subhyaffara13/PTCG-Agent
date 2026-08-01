
def test_bound_method_callback():
    # Bound Python method:
    class MyClass:
        def double(self, val):
            return 2 * val

    z = MyClass()
    assert m.test_callback3(z.double) == "func(43) = 86"

    z = m.CppBoundMethodTest()
    assert m.test_callback3(z.triple) == "func(43) = 129"

