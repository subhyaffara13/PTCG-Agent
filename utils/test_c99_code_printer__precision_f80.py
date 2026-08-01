
def test_C99CodePrinter__precision_f80():
    f80_printer = C99CodePrinter({"type_aliases": {real: float80}})
    assert f80_printer.doprint(sin(x + Float('2.1'))) == 'sinl(x + 2.1L)'

