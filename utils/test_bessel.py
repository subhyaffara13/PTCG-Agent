
def test_bessel():
    from sympy.functions.special.bessel import (besseli, besselj)
    assert simplify(integrate(besselj(a, z)*besselj(b, z)/z, (z, 0, oo),
                     meijerg=True, conds='none')) == \
        2*sin(pi*(a/2 - b/2))/(pi*(a - b)*(a + b))
    assert simplify(integrate(besselj(a, z)*besselj(a, z)/z, (z, 0, oo),
                     meijerg=True, conds='none')) == 1/(2*a)

    # TODO more orthogonality integrals

    assert simplify(integrate(sin(z*x)*(x**2 - 1)**(-(y + S.Half)),
                              (x, 1, oo), meijerg=True, conds='none')
                    *2/((z/2)**y*sqrt(pi)*gamma(S.Half - y))) == \
        besselj(y, z)

    # Werner Rosenheinrich
    # SOME INDEFINITE INTEGRALS OF BESSEL FUNCTIONS

    assert integrate(x*besselj(0, x), x, meijerg=True) == x*besselj(1, x)
    assert integrate(x*besseli(0, x), x, meijerg=True) == x*besseli(1, x)
    # TODO can do higher powers, but come out as high order ... should they be
    #      reduced to order 0, 1?
    assert integrate(besselj(1, x), x, meijerg=True) == -besselj(0, x)
    assert integrate(besselj(1, x)**2/x, x, meijerg=True) == \
        -(besselj(0, x)**2 + besselj(1, x)**2)/2
    # TODO more besseli when tables are extended or recursive mellin works
    assert integrate(besselj(0, x)**2/x**2, x, meijerg=True) == \
        -2*x*besselj(0, x)**2 - 2*x*besselj(1, x)**2 \
        + 2*besselj(0, x)*besselj(1, x) - besselj(0, x)**2/x
    assert integrate(besselj(0, x)*besselj(1, x), x, meijerg=True) == \
        -besselj(0, x)**2/2
    assert integrate(x**2*besselj(0, x)*besselj(1, x), x, meijerg=True) == \
        x**2*besselj(1, x)**2/2
    assert integrate(besselj(0, x)*besselj(1, x)/x, x, meijerg=True) == \
        (x*besselj(0, x)**2 + x*besselj(1, x)**2 -
            besselj(0, x)*besselj(1, x))
    # TODO how does besselj(0, a*x)*besselj(0, b*x) work?
    # TODO how does besselj(0, x)**2*besselj(1, x)**2 work?
    # TODO sin(x)*besselj(0, x) etc come out a mess
    # TODO can x*log(x)*besselj(0, x) be done?
    # TODO how does besselj(1, x)*besselj(0, x+a) work?
    # TODO more indefinite integrals when struve functions etc are implemented

    # test a substitution
    assert integrate(besselj(1, x**2)*x, x, meijerg=True) == \
        -besselj(0, x**2)/2


def test_bessel():
    mp.dps = 15
    assert j0(1).ae(0.765197686557966551)
    assert j0(pi).ae(-0.304242177644093864)
    assert j0(1000).ae(0.0247866861524201746)
    assert j0(-25).ae(0.0962667832759581162)
    assert j1(1).ae(0.440050585744933516)
    assert j1(pi).ae(0.284615343179752757)
    assert j1(1000).ae(0.00472831190708952392)
    assert j1(-25).ae(0.125350249580289905)
    assert besselj(5,1).ae(0.000249757730211234431)
    assert besselj(5+0j,1).ae(0.000249757730211234431)
    assert besselj(5,pi).ae(0.0521411843671184747)
    assert besselj(5,1000).ae(0.00502540694523318607)
    assert besselj(5,-25).ae(0.0660079953984229934)
    assert besselj(-3,2).ae(-0.128943249474402051)
    assert besselj(-4,2).ae(0.0339957198075684341)
    assert besselj(3,3+2j).ae(0.424718794929639595942 + 0.625665327745785804812j)
    assert besselj(0.25,4).ae(-0.374760630804249715)
    assert besselj(1+2j,3+4j).ae(0.319247428741872131 - 0.669557748880365678j)
    assert (besselj(3, 10**10) * 10**5).ae(0.76765081748139204023)
    assert bessely(-0.5, 0) == 0
    assert bessely(0.5, 0) == -inf
    assert bessely(1.5, 0) == -inf
    assert bessely(0,0) == -inf
    assert bessely(-0.4, 0) == -inf
    assert bessely(-0.6, 0) == inf
    assert bessely(-1, 0) == inf
    assert bessely(-1.4, 0) == inf
    assert bessely(-1.6, 0) == -inf
    assert bessely(-1, 0) == inf
    assert bessely(-2, 0) == -inf
    assert bessely(-3, 0) == inf
    assert bessely(0.5, 0) == -inf
    assert bessely(1, 0) == -inf
    assert bessely(1.5, 0) == -inf
    assert bessely(2, 0) == -inf
    assert bessely(2.5, 0) == -inf
    assert bessely(3, 0) == -inf
    assert bessely(0,0.5).ae(-0.44451873350670655715)
    assert bessely(1,0.5).ae(-1.4714723926702430692)
    assert bessely(-1,0.5).ae(1.4714723926702430692)
    assert bessely(3.5,0.5).ae(-138.86400867242488443)
    assert bessely(0,3+4j).ae(4.6047596915010138655-8.8110771408232264208j)
    assert bessely(0,j).ae(-0.26803248203398854876+1.26606587775200833560j)
    assert (bessely(3, 10**10) * 10**5).ae(0.21755917537013204058)
    assert besseli(0,0) == 1
    assert besseli(1,0) == 0
    assert besseli(2,0) == 0
    assert besseli(-1,0) == 0
    assert besseli(-2,0) == 0
    assert besseli(0,0.5).ae(1.0634833707413235193)
    assert besseli(1,0.5).ae(0.25789430539089631636)
    assert besseli(-1,0.5).ae(0.25789430539089631636)
    assert besseli(3.5,0.5).ae(0.00068103597085793815863)
    assert besseli(0,3+4j).ae(-3.3924877882755196097-1.3239458916287264815j)
    assert besseli(0,j).ae(besselj(0,1))
    assert (besseli(3, 10**10) * mpf(10)**(-4342944813)).ae(4.2996028505491271875)
    assert besselk(0,0) == inf
    assert besselk(1,0) == inf
    assert besselk(2,0) == inf
    assert besselk(-1,0) == inf
    assert besselk(-2,0) == inf
    assert besselk(0,0.5).ae(0.92441907122766586178)
    assert besselk(1,0.5).ae(1.6564411200033008937)
    assert besselk(-1,0.5).ae(1.6564411200033008937)
    assert besselk(3.5,0.5).ae(207.48418747548460607)
    assert besselk(0,3+4j).ae(-0.007239051213570155013+0.026510418350267677215j)
    assert besselk(0,j).ae(-0.13863371520405399968-1.20196971531720649914j)
    assert (besselk(3, 10**10) * mpf(10)**4342944824).ae(1.1628981033356187851)
    # test for issue 331, bug reported by Michael Hartmann
    for n in range(10,100,10):
        mp.dps = n
        assert besseli(91.5,24.7708).ae("4.00830632138673963619656140653537080438462342928377020695738635559218797348548092636896796324190271316137982810144874264e-41")

