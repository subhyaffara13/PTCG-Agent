
def test_fps__compose():
    f1, f2, f3 = fps(exp(x)), fps(sin(x)), fps(cos(x))

    raises(ValueError, lambda: f1.compose(sin(x), x))
    raises(ValueError, lambda: f1.compose(fps(sin(x), dir=-1), x, 4))
    raises(ValueError, lambda: f1.compose(fps(sin(x), x0=1), x, 4))
    raises(ValueError, lambda: f1.compose(fps(sin(y)), x, 4))

    raises(ValueError, lambda: f1.compose(f3, x))
    raises(ValueError, lambda: f2.compose(f3, x))

    fcomp = f1.compose(f2, x)
    assert isinstance(fcomp, FormalPowerSeriesCompose)
    assert isinstance(fcomp.ffps, FormalPowerSeries)
    assert isinstance(fcomp.gfps, FormalPowerSeries)
    assert fcomp.f == exp(x)
    assert fcomp.g == sin(x)
    assert fcomp.function == exp(sin(x))
    assert fcomp._eval_terms(6) == 1 + x + x**2/2 - x**4/8 - x**5/15
    assert fcomp.truncate() == 1 + x + x**2/2 - x**4/8 - x**5/15 + O(x**6)
    assert fcomp.truncate(5) == 1 + x + x**2/2 - x**4/8 + O(x**5)

    raises(NotImplementedError, lambda: fcomp._eval_term(5))
    raises(NotImplementedError, lambda: fcomp.infinite)
    raises(NotImplementedError, lambda: fcomp._eval_derivative(x))
    raises(NotImplementedError, lambda: fcomp.integrate(x))

    assert f1.compose(f2, x).truncate(4) == 1 + x + x**2/2 + O(x**4)
    assert f1.compose(f2, x).truncate(8) == \
        1 + x + x**2/2 - x**4/8 - x**5/15 - x**6/240 + x**7/90 + O(x**8)
    assert f1.compose(f2, x).truncate(6) == \
        1 + x + x**2/2 - x**4/8 - x**5/15 + O(x**6)

    assert f2.compose(f2, x).truncate(4) == x - x**3/3 + O(x**4)
    assert f2.compose(f2, x).truncate(8) == x - x**3/3 + x**5/10 - 8*x**7/315 + O(x**8)
    assert f2.compose(f2, x).truncate(6) == x - x**3/3 + x**5/10 + O(x**6)

