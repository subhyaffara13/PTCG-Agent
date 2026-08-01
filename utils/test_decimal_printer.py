
def test_decimal_printer():
    dec_printer = StrPrinter(settings={"dps":3})
    f = Function('f')
    assert dec_printer.doprint(f(1.329294)) == "f(1.33)"

