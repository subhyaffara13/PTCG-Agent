
def test_evalf_bugs():
    assert NS(sin(1) + exp(-10**10), 10) == NS(sin(1), 10)
    assert NS(exp(10**10) + sin(1), 10) == NS(exp(10**10), 10)
    assert NS('expand_log(log(1+1/10**50))', 20) == '1.0000000000000000000e-50'
    assert NS('log(10**100,10)', 10) == '100.0000000'
    assert NS('log(2)', 10) == '0.6931471806'
    assert NS(
        '(sin(x)-x)/x**3', 15, subs={x: '1/10**50'}) == '-0.166666666666667'
    assert NS(sin(1) + Rational(
        1, 10**100)*I, 15) == '0.841470984807897 + 1.00000000000000e-100*I'
    assert x.evalf() == x
    assert NS((1 + I)**2*I, 6) == '-2.00000'
    d = {n: (
        -1)**Rational(6, 7), y: (-1)**Rational(4, 7), x: (-1)**Rational(2, 7)}
    assert NS((x*(1 + y*(1 + n))).subs(d).evalf(), 6) == '0.346011 + 0.433884*I'
    assert NS(((-I - sqrt(2)*I)**2).evalf()) == '-5.82842712474619'
    assert NS((1 + I)**2*I, 15) == '-2.00000000000000'
    # issue 4758 (1/2):
    assert NS(pi.evalf(69) - pi) == '-4.43863937855894e-71'
    # issue 4758 (2/2): With the bug present, this still only fails if the
    # terms are in the order given here. This is not generally the case,
    # because the order depends on the hashes of the terms.
    assert NS(20 - 5008329267844*n**25 - 477638700*n**37 - 19*n,
              subs={n: .01}) == '19.8100000000000'
    assert NS(((x - 1)*(1 - x)**1000).n()
              ) == '(1.00000000000000 - x)**1000*(x - 1.00000000000000)'
    assert NS((-x).n()) == '-x'
    assert NS((-2*x).n()) == '-2.00000000000000*x'
    assert NS((-2*x*y).n()) == '-2.00000000000000*x*y'
    assert cos(x).n(subs={x: 1+I}) == cos(x).subs(x, 1+I).n()
    # issue 6660. Also NaN != mpmath.nan
    # In this order:
    # 0*nan, 0/nan, 0*inf, 0/inf
    # 0+nan, 0-nan, 0+inf, 0-inf
    # >>> n = Some Number
    # n*nan, n/nan, n*inf, n/inf
    # n+nan, n-nan, n+inf, n-inf
    assert (0*E**(oo)).n() is S.NaN
    assert (0/E**(oo)).n() is S.Zero

    assert (0+E**(oo)).n() is S.Infinity
    assert (0-E**(oo)).n() is S.NegativeInfinity

    assert (5*E**(oo)).n() is S.Infinity
    assert (5/E**(oo)).n() is S.Zero

    assert (5+E**(oo)).n() is S.Infinity
    assert (5-E**(oo)).n() is S.NegativeInfinity

    #issue 7416
    assert as_mpmath(0.0, 10, {'chop': True}) == 0

    #issue 5412
    assert ((oo*I).n() == S.Infinity*I)
    assert ((oo+oo*I).n() == S.Infinity + S.Infinity*I)

    #issue 11518
    assert NS(2*x**2.5, 5) == '2.0000*x**2.5000'

    #issue 13076
    assert NS(Mul(Max(0, y), x, evaluate=False).evalf()) == 'x*Max(0, y)'

    #issue 18516
    assert NS(log(S(3273390607896141870013189696827599152216642046043064789483291368096133796404674554883270092325904157150886684127560071009217256545885393053328527589376)/36360291795869936842385267079543319118023385026001623040346035832580600191583895484198508262979388783308179702534403855752855931517013066142992430916562025780021771247847643450125342836565813209972590371590152578728008385990139795377610001).evalf(15, chop=True)) == '-oo'

