
def test_lerchphi():
    from sympy.functions.special.zeta_functions import (lerchphi, polylog)
    from sympy.simplify.gammasimp import gammasimp
    assert hyperexpand(hyper([1, a], [a + 1], z)/a) == lerchphi(z, 1, a)
    assert hyperexpand(
        hyper([1, a, a], [a + 1, a + 1], z)/a**2) == lerchphi(z, 2, a)
    assert hyperexpand(hyper([1, a, a, a], [a + 1, a + 1, a + 1], z)/a**3) == \
        lerchphi(z, 3, a)
    assert hyperexpand(hyper([1] + [a]*10, [a + 1]*10, z)/a**10) == \
        lerchphi(z, 10, a)
    assert gammasimp(hyperexpand(meijerg([0, 1 - a], [], [0],
        [-a], exp_polar(-I*pi)*z))) == lerchphi(z, 1, a)
    assert gammasimp(hyperexpand(meijerg([0, 1 - a, 1 - a], [], [0],
        [-a, -a], exp_polar(-I*pi)*z))) == lerchphi(z, 2, a)
    assert gammasimp(hyperexpand(meijerg([0, 1 - a, 1 - a, 1 - a], [], [0],
        [-a, -a, -a], exp_polar(-I*pi)*z))) == lerchphi(z, 3, a)

    assert hyperexpand(z*hyper([1, 1], [2], z)) == -log(1 + -z)
    assert hyperexpand(z*hyper([1, 1, 1], [2, 2], z)) == polylog(2, z)
    assert hyperexpand(z*hyper([1, 1, 1, 1], [2, 2, 2], z)) == polylog(3, z)

    assert hyperexpand(hyper([1, a, 1 + S.Half], [a + 1, S.Half], z)) == \
        -2*a/(z - 1) + (-2*a**2 + a)*lerchphi(z, 1, a)

    # Now numerical tests. These make sure reductions etc are carried out
    # correctly

    # a rational function (polylog at negative integer order)
    assert can_do([2, 2, 2], [1, 1])

    # NOTE these contain log(1-x) etc ... better make sure we have |z| < 1
    # reduction of order for polylog
    assert can_do([1, 1, 1, b + 5], [2, 2, b], div=10)

    # reduction of order for lerchphi
    # XXX lerchphi in mpmath is flaky
    assert can_do(
        [1, a, a, a, b + 5], [a + 1, a + 1, a + 1, b], numerical=False)

    # test a bug
    from sympy.functions.elementary.complexes import Abs
    assert hyperexpand(hyper([S.Half, S.Half, S.Half, 1],
                             [Rational(3, 2), Rational(3, 2), Rational(3, 2)], Rational(1, 4))) == \
        Abs(-polylog(3, exp_polar(I*pi)/2) + polylog(3, S.Half))

