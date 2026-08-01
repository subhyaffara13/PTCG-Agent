
def test_mathml_printer():
    m = MathMLPrinter()
    assert m.doprint(1+x) == mp.doprint(1+x)

