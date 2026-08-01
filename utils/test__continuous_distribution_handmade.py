
def test_ContinuousDistributionHandmade():
    x = Symbol('x')
    z = Dummy('z')
    dens = Lambda(x, Piecewise((S.Half, (0<=x)&(x<1)), (0, (x>=1)&(x<2)),
        (S.Half, (x>=2)&(x<3)), (0, True)))
    dens = ContinuousDistributionHandmade(dens, set=Interval(0, 3))
    space = SingleContinuousPSpace(z, dens)
    assert dens.pdf == Lambda(x, Piecewise((S(1)/2, (x >= 0) & (x < 1)),
        (0, (x >= 1) & (x < 2)), (S(1)/2, (x >= 2) & (x < 3)), (0, True)))
    assert median(space.value) == Interval(1, 2)
    assert E(space.value) == Rational(3, 2)
    assert variance(space.value) == Rational(13, 12)

