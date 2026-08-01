
def test_ccode_Declaration():
    i = symbols('i', integer=True)
    var1 = Variable(i, type=Type.from_expr(i))
    dcl1 = Declaration(var1)
    assert ccode(dcl1) == 'int i'

    var2 = Variable(x, type=float32, attrs={value_const})
    dcl2a = Declaration(var2)
    assert ccode(dcl2a) == 'const float x'
    dcl2b = var2.as_Declaration(value=pi)
    assert ccode(dcl2b) == 'const float x = M_PI'

    var3 = Variable(y, type=Type('bool'))
    dcl3 = Declaration(var3)
    printer = C89CodePrinter()
    assert 'stdbool.h' not in printer.headers
    assert printer.doprint(dcl3) == 'bool y'
    assert 'stdbool.h' in printer.headers

    u = symbols('u', real=True)
    ptr4 = Pointer.deduced(u, attrs={pointer_const, restrict})
    dcl4 = Declaration(ptr4)
    assert ccode(dcl4) == 'double * const restrict u'

    var5 = Variable(x, Type('__float128'), attrs={value_const})
    dcl5a = Declaration(var5)
    assert ccode(dcl5a) == 'const __float128 x'
    var5b = Variable(var5.symbol, var5.type, pi, attrs=var5.attrs)
    dcl5b = Declaration(var5b)
    assert ccode(dcl5b) == 'const __float128 x = M_PI'

