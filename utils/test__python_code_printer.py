
def test_PythonCodePrinter():
    prntr = PythonCodePrinter()

    assert not prntr.module_imports

    assert prntr.doprint(x**y) == 'x**y'
    assert prntr.doprint(Mod(x, 2)) == 'x % 2'
    assert prntr.doprint(-Mod(x, y)) == '-(x % y)'
    assert prntr.doprint(Mod(-x, y)) == '(-x) % y'
    assert prntr.doprint(And(x, y)) == 'x and y'
    assert prntr.doprint(Or(x, y)) == 'x or y'
    assert prntr.doprint(1/(x+y)) == '1/(x + y)'
    assert prntr.doprint(Not(x)) == 'not x'
    assert not prntr.module_imports

    assert prntr.doprint(pi) == 'math.pi'
    assert prntr.module_imports == {'math': {'pi'}}

    assert prntr.doprint(x**Rational(1, 2)) == 'math.sqrt(x)'
    assert prntr.doprint(sqrt(x)) == 'math.sqrt(x)'
    assert prntr.module_imports == {'math': {'pi', 'sqrt'}}

    assert prntr.doprint(acos(x)) == 'math.acos(x)'
    assert prntr.doprint(cot(x)) == '(1/math.tan(x))'
    assert prntr.doprint(coth(x)) == '((math.exp(x) + math.exp(-x))/(math.exp(x) - math.exp(-x)))'
    assert prntr.doprint(asec(x)) == '(math.acos(1/x))'
    assert prntr.doprint(acsch(x)) == '(math.log(math.sqrt(1 + x**(-2)) + 1/x))'

    assert prntr.doprint(Assignment(x, 2)) == 'x = 2'
    assert prntr.doprint(Piecewise((1, Eq(x, 0)),
                        (2, x>6))) == '((1) if (x == 0) else (2) if (x > 6) else None)'
    assert prntr.doprint(Piecewise((2, Le(x, 0)),
                        (3, Gt(x, 0)), evaluate=False)) == '((2) if (x <= 0) else'\
                                                        ' (3) if (x > 0) else None)'
    assert prntr.doprint(sign(x)) == '(0.0 if x == 0 else math.copysign(1, x))'
    assert prntr.doprint(p[0, 1]) == 'p[0, 1]'
    assert prntr.doprint(KroneckerDelta(x,y)) == '(1 if x == y else 0)'

    assert prntr.doprint((2,3)) == "(2, 3)"
    assert prntr.doprint([2,3]) == "[2, 3]"

    assert prntr.doprint(Min(x, y)) == "min(x, y)"
    assert prntr.doprint(Max(x, y)) == "max(x, y)"

