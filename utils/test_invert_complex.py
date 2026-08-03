from typing import Union

def test_invert_complex():
    assert invert_complex(x + 3, y, x) == (x, FiniteSet(y - 3))
    assert invert_complex(x*3, y, x) == (x, FiniteSet(y / 3))
    assert invert_complex((x - 1)**3, 0, x) == (x, FiniteSet(1))

    assert dumeq(invert_complex(exp(x), y, x),
        (x, imageset(Lambda(n, I*(2*pi*n + arg(y)) + log(Abs(y))), S.Integers)))

    assert invert_complex(log(x), y, x) == (x, FiniteSet(exp(y)))

    raises(ValueError, lambda: invert_real(1, y, x))
    raises(ValueError, lambda: invert_complex(x, x, x))
    raises(ValueError, lambda: invert_complex(x, x, 1))

    assert dumeq(invert_complex(sin(x), I, x), (x, Union(
        ImageSet(Lambda(n, 2*n*pi + I*log(1 + sqrt(2))), S.Integers),
        ImageSet(Lambda(n, 2*n*pi + pi - I*log(1 + sqrt(2))), S.Integers))))
    assert dumeq(invert_complex(cos(x), 1+I, x), (x, Union(
        ImageSet(Lambda(n, 2*n*pi - acos(1 + I)), S.Integers),
        ImageSet(Lambda(n, 2*n*pi + acos(1 + I)), S.Integers))))
    assert dumeq(invert_complex(tan(2*x), 1, x), (x,
        ImageSet(Lambda(n, n*pi/2 + pi/8), S.Integers)))
    assert dumeq(invert_complex(cot(x), 2*I, x), (x,
        ImageSet(Lambda(n, n*pi - I*acoth(2)), S.Integers)))

    assert dumeq(invert_complex(sinh(x), 0, x), (x, Union(
        ImageSet(Lambda(n, 2*n*I*pi), S.Integers),
        ImageSet(Lambda(n, 2*n*I*pi + I*pi), S.Integers))))
    assert dumeq(invert_complex(cosh(x), 0, x), (x, Union(
        ImageSet(Lambda(n, 2*n*I*pi + I*pi/2), S.Integers),
        ImageSet(Lambda(n, 2*n*I*pi + 3*I*pi/2), S.Integers))))
    assert invert_complex(tanh(x), 1, x) == (x, S.EmptySet)
    assert dumeq(invert_complex(tanh(x), a, x), (x,
        ConditionSet(x, Ne(a, -1) & Ne(a, 1),
        ImageSet(Lambda(n, n*I*pi + atanh(a)), S.Integers))))
    assert invert_complex(coth(x), 1, x) == (x, S.EmptySet)
    assert dumeq(invert_complex(coth(x), a, x), (x,
        ConditionSet(x, Ne(a, -1) & Ne(a, 1),
        ImageSet(Lambda(n, n*I*pi + acoth(a)), S.Integers))))
    assert dumeq(invert_complex(sech(x), 2, x), (x, Union(
        ImageSet(Lambda(n, 2*n*I*pi + I*pi/3), S.Integers),
        ImageSet(Lambda(n, 2*n*I*pi + 5*I*pi/3), S.Integers))))

