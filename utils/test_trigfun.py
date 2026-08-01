
def test_trigfun():
    for f in (sin, cos, tan, cot, sec, csc, asin, acos, acot, atan, asec, acsc,
              sinh, cosh, tanh, coth, csch, sech, asinh, acosh, atanh, acoth,
              asech, acsch):
        assert octave_code(f(x) == f.__name__ + '(x)')

