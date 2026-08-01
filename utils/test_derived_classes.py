
def test_derived_classes():
    class MyFancyFCodePrinter(FCodePrinter):
        _default_settings = FCodePrinter._default_settings.copy()

    printer = MyFancyFCodePrinter()
    x = symbols('x')
    assert printer.doprint(sin(x), "bork") == "      bork = sin(x)"

