
def test_cupy_print():
    prntr = CuPyPrinter()
    assert prntr.doprint(logaddexp(a, b)) == 'cupy.logaddexp(a, b)'
    assert prntr.doprint(sqrt(x)) == 'cupy.sqrt(x)'
    assert prntr.doprint(log(x)) == 'cupy.log(x)'
    assert prntr.doprint("acos(x)") == 'cupy.arccos(x)'
    assert prntr.doprint("exp(x)") == 'cupy.exp(x)'
    assert prntr.doprint("Abs(x)") == 'abs(x)'

