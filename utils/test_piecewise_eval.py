
def test_piecewise_eval():
    # XXX these tests might need modification if this
    # simplification is moved out of eval and into
    # boolalg or Piecewise simplification functions
    f = lambda x: x.args[0].cond
    # unsimplified
    assert f(Piecewise((x, (x > -oo) & (x < 3)))
        ) == ((x > -oo) & (x < 3))
    assert f(Piecewise((x, (x > -oo) & (x < oo)))
        ) == ((x > -oo) & (x < oo))
    assert f(Piecewise((x, (x > -3) & (x < 3)))
        ) == ((x > -3) & (x < 3))
    assert f(Piecewise((x, (x > -3) & (x < oo)))
        ) == ((x > -3) & (x < oo))
    assert f(Piecewise((x, (x <= 3) & (x > -oo)))
        ) == ((x <= 3) & (x > -oo))
    assert f(Piecewise((x, (x <= 3) & (x > -3)))
        ) == ((x <= 3) & (x > -3))
    assert f(Piecewise((x, (x >= -3) & (x < 3)))
        ) == ((x >= -3) & (x < 3))
    assert f(Piecewise((x, (x >= -3) & (x < oo)))
        ) == ((x >= -3) & (x < oo))
    assert f(Piecewise((x, (x >= -3) & (x <= 3)))
        ) == ((x >= -3) & (x <= 3))
    # could simplify by keeping only the first
    # arg of result
    assert f(Piecewise((x, (x <= oo) & (x > -oo)))
        ) == (x > -oo) & (x <= oo)
    assert f(Piecewise((x, (x <= oo) & (x > -3)))
        ) == (x > -3) & (x <= oo)
    assert f(Piecewise((x, (x >= -oo) & (x < 3)))
        ) == (x < 3) & (x >= -oo)
    assert f(Piecewise((x, (x >= -oo) & (x < oo)))
        ) == (x < oo) & (x >= -oo)
    assert f(Piecewise((x, (x >= -oo) & (x <= 3)))
        ) == (x <= 3) & (x >= -oo)
    assert f(Piecewise((x, (x >= -oo) & (x <= oo)))
        ) == (x <= oo) & (x >= -oo)  # but cannot be True unless x is real
    assert f(Piecewise((x, (x >= -3) & (x <= oo)))
        ) == (x >= -3) & (x <= oo)
    assert f(Piecewise((x, (Abs(arg(a)) <= 1) | (Abs(arg(a)) < 1)))
        ) == (Abs(arg(a)) <= 1) | (Abs(arg(a)) < 1)

