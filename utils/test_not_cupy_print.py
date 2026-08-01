
def test_not_cupy_print():
    prntr = CuPyPrinter()
    with raises(NotImplementedError):
        prntr.doprint("abcd(x)")

