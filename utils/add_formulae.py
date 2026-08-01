
def add_formulae(formulae):
    """ Create our knowledge base. """
    a, b, c, z = symbols('a b c, z', cls=Dummy)

    def add(ap, bq, res):
        func = Hyper_Function(ap, bq)
        formulae.append(Formula(func, z, res, (a, b, c)))

    def addb(ap, bq, B, C, M):
        func = Hyper_Function(ap, bq)
        formulae.append(Formula(func, z, None, (a, b, c), B, C, M))

    # Luke, Y. L. (1969), The Special Functions and Their Approximations,
    # Volume 1, section 6.2

    # 0F0
    add((), (), exp(z))

    # 1F0
    add((a, ), (), HyperRep_power1(-a, z))

    # 2F1
    addb((a, a - S.Half), (2*a, ),
         Matrix([HyperRep_power2(a, z),
                 HyperRep_power2(a + S.Half, z)/2]),
         Matrix([[1, 0]]),
         Matrix([[(a - S.Half)*z/(1 - z), (S.Half - a)*z/(1 - z)],
                 [a/(1 - z), a*(z - 2)/(1 - z)]]))
    addb((1, 1), (2, ),
         Matrix([HyperRep_log1(z), 1]), Matrix([[-1/z, 0]]),
         Matrix([[0, z/(z - 1)], [0, 0]]))
    addb((S.Half, 1), (S('3/2'), ),
         Matrix([HyperRep_atanh(z), 1]),
         Matrix([[1, 0]]),
         Matrix([[Rational(-1, 2), 1/(1 - z)/2], [0, 0]]))
    addb((S.Half, S.Half), (S('3/2'), ),
         Matrix([HyperRep_asin1(z), HyperRep_power1(Rational(-1, 2), z)]),
         Matrix([[1, 0]]),
         Matrix([[Rational(-1, 2), S.Half], [0, z/(1 - z)/2]]))
    addb((a, S.Half + a), (S.Half, ),
         Matrix([HyperRep_sqrts1(-a, z), -HyperRep_sqrts2(-a - S.Half, z)]),
         Matrix([[1, 0]]),
         Matrix([[0, -a],
                 [z*(-2*a - 1)/2/(1 - z), S.Half - z*(-2*a - 1)/(1 - z)]]))

    # A. P. Prudnikov, Yu. A. Brychkov and O. I. Marichev (1990).
    # Integrals and Series: More Special Functions, Vol. 3,.
    # Gordon and Breach Science Publisher
    addb([a, -a], [S.Half],
         Matrix([HyperRep_cosasin(a, z), HyperRep_sinasin(a, z)]),
         Matrix([[1, 0]]),
         Matrix([[0, -a], [a*z/(1 - z), 1/(1 - z)/2]]))
    addb([1, 1], [3*S.Half],
         Matrix([HyperRep_asin2(z), 1]), Matrix([[1, 0]]),
         Matrix([[(z - S.Half)/(1 - z), 1/(1 - z)/2], [0, 0]]))

    # Complete elliptic integrals K(z) and E(z), both a 2F1 function
    addb([S.Half, S.Half], [S.One],
         Matrix([elliptic_k(z), elliptic_e(z)]),
         Matrix([[2/pi, 0]]),
         Matrix([[Rational(-1, 2), -1/(2*z-2)],
                 [Rational(-1, 2), S.Half]]))
    addb([Rational(-1, 2), S.Half], [S.One],
         Matrix([elliptic_k(z), elliptic_e(z)]),
         Matrix([[0, 2/pi]]),
         Matrix([[Rational(-1, 2), -1/(2*z-2)],
                 [Rational(-1, 2), S.Half]]))

    # 3F2
    addb([Rational(-1, 2), 1, 1], [S.Half, 2],
         Matrix([z*HyperRep_atanh(z), HyperRep_log1(z), 1]),
         Matrix([[Rational(-2, 3), -S.One/(3*z), Rational(2, 3)]]),
         Matrix([[S.Half, 0, z/(1 - z)/2],
                 [0, 0, z/(z - 1)],
                 [0, 0, 0]]))
    # actually the formula for 3/2 is much nicer ...
    addb([Rational(-1, 2), 1, 1], [2, 2],
         Matrix([HyperRep_power1(S.Half, z), HyperRep_log2(z), 1]),
         Matrix([[Rational(4, 9) - 16/(9*z), 4/(3*z), 16/(9*z)]]),
         Matrix([[z/2/(z - 1), 0, 0], [1/(2*(z - 1)), 0, S.Half], [0, 0, 0]]))

    # 1F1
    addb([1], [b], Matrix([z**(1 - b) * exp(z) * lowergamma(b - 1, z), 1]),
         Matrix([[b - 1, 0]]), Matrix([[1 - b + z, 1], [0, 0]]))
    addb([a], [2*a],
         Matrix([z**(S.Half - a)*exp(z/2)*besseli(a - S.Half, z/2)
                 * gamma(a + S.Half)/4**(S.Half - a),
                 z**(S.Half - a)*exp(z/2)*besseli(a + S.Half, z/2)
                 * gamma(a + S.Half)/4**(S.Half - a)]),
         Matrix([[1, 0]]),
         Matrix([[z/2, z/2], [z/2, (z/2 - 2*a)]]))
    mz = polar_lift(-1)*z
    addb([a], [a + 1],
         Matrix([mz**(-a)*a*lowergamma(a, mz), a*exp(z)]),
         Matrix([[1, 0]]),
         Matrix([[-a, 1], [0, z]]))
    # This one is redundant.
    add([Rational(-1, 2)], [S.Half], exp(z) - sqrt(pi*z)*(-I)*erf(I*sqrt(z)))

    # Added to get nice results for Laplace transform of Fresnel functions
    # https://functions.wolfram.com/07.22.03.6437.01
    # Basic rule
    #add([1], [Rational(3, 4), Rational(5, 4)],
    #    sqrt(pi) * (cos(2*sqrt(polar_lift(-1)*z))*fresnelc(2*root(polar_lift(-1)*z,4)/sqrt(pi)) +
    #                sin(2*sqrt(polar_lift(-1)*z))*fresnels(2*root(polar_lift(-1)*z,4)/sqrt(pi)))
    #    / (2*root(polar_lift(-1)*z,4)))
    # Manually tuned rule
    addb([1], [Rational(3, 4), Rational(5, 4)],
         Matrix([ sqrt(pi)*(I*sinh(2*sqrt(z))*fresnels(2*root(z, 4)*exp(I*pi/4)/sqrt(pi))
                            + cosh(2*sqrt(z))*fresnelc(2*root(z, 4)*exp(I*pi/4)/sqrt(pi)))
                  * exp(-I*pi/4)/(2*root(z, 4)),
                  sqrt(pi)*root(z, 4)*(sinh(2*sqrt(z))*fresnelc(2*root(z, 4)*exp(I*pi/4)/sqrt(pi))
                                      + I*cosh(2*sqrt(z))*fresnels(2*root(z, 4)*exp(I*pi/4)/sqrt(pi)))
                  *exp(-I*pi/4)/2,
                  1 ]),
         Matrix([[1, 0, 0]]),
         Matrix([[Rational(-1, 4),              1, Rational(1, 4)],
                 [              z, Rational(1, 4),              0],
                 [              0,              0,              0]]))

    # 2F2
    addb([S.Half, a], [Rational(3, 2), a + 1],
         Matrix([a/(2*a - 1)*(-I)*sqrt(pi/z)*erf(I*sqrt(z)),
                 a/(2*a - 1)*(polar_lift(-1)*z)**(-a)*
                 lowergamma(a, polar_lift(-1)*z),
                 a/(2*a - 1)*exp(z)]),
         Matrix([[1, -1, 0]]),
         Matrix([[Rational(-1, 2), 0, 1], [0, -a, 1], [0, 0, z]]))
    # We make a "basis" of four functions instead of three, and give EulerGamma
    # an extra slot (it could just be a coefficient to 1). The advantage is
    # that this way Polys will not see multivariate polynomials (it treats
    # EulerGamma as an indeterminate), which is *way* faster.
    addb([1, 1], [2, 2],
         Matrix([Ei(z) - log(z), exp(z), 1, EulerGamma]),
         Matrix([[1/z, 0, 0, -1/z]]),
         Matrix([[0, 1, -1, 0], [0, z, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]))

    # 0F1
    add((), (S.Half, ), cosh(2*sqrt(z)))
    addb([], [b],
         Matrix([gamma(b)*z**((1 - b)/2)*besseli(b - 1, 2*sqrt(z)),
                 gamma(b)*z**(1 - b/2)*besseli(b, 2*sqrt(z))]),
         Matrix([[1, 0]]), Matrix([[0, 1], [z, (1 - b)]]))

    # 0F3
    x = 4*z**Rational(1, 4)

    def fp(a, z):
        return besseli(a, x) + besselj(a, x)

    def fm(a, z):
        return besseli(a, x) - besselj(a, x)

    # TODO branching
    addb([], [S.Half, a, a + S.Half],
         Matrix([fp(2*a - 1, z), fm(2*a, z)*z**Rational(1, 4),
                 fm(2*a - 1, z)*sqrt(z), fp(2*a, z)*z**Rational(3, 4)])
         * 2**(-2*a)*gamma(2*a)*z**((1 - 2*a)/4),
         Matrix([[1, 0, 0, 0]]),
         Matrix([[0, 1, 0, 0],
                 [0, S.Half - a, 1, 0],
                 [0, 0, S.Half, 1],
                 [z, 0, 0, 1 - a]]))
    x = 2*(4*z)**Rational(1, 4)*exp_polar(I*pi/4)
    addb([], [a, a + S.Half, 2*a],
         (2*sqrt(polar_lift(-1)*z))**(1 - 2*a)*gamma(2*a)**2 *
         Matrix([besselj(2*a - 1, x)*besseli(2*a - 1, x),
                 x*(besseli(2*a, x)*besselj(2*a - 1, x)
                    - besseli(2*a - 1, x)*besselj(2*a, x)),
                 x**2*besseli(2*a, x)*besselj(2*a, x),
                 x**3*(besseli(2*a, x)*besselj(2*a - 1, x)
                       + besseli(2*a - 1, x)*besselj(2*a, x))]),
         Matrix([[1, 0, 0, 0]]),
         Matrix([[0, Rational(1, 4), 0, 0],
                 [0, (1 - 2*a)/2, Rational(-1, 2), 0],
                 [0, 0, 1 - 2*a, Rational(1, 4)],
                 [-32*z, 0, 0, 1 - a]]))

    # 1F2
    addb([a], [a - S.Half, 2*a],
         Matrix([z**(S.Half - a)*besseli(a - S.Half, sqrt(z))**2,
                 z**(1 - a)*besseli(a - S.Half, sqrt(z))
                 *besseli(a - Rational(3, 2), sqrt(z)),
                 z**(Rational(3, 2) - a)*besseli(a - Rational(3, 2), sqrt(z))**2]),
         Matrix([[-gamma(a + S.Half)**2/4**(S.Half - a),
                 2*gamma(a - S.Half)*gamma(a + S.Half)/4**(1 - a),
                 0]]),
         Matrix([[1 - 2*a, 1, 0], [z/2, S.Half - a, S.Half], [0, z, 0]]))
    addb([S.Half], [b, 2 - b],
         pi*(1 - b)/sin(pi*b)*
         Matrix([besseli(1 - b, sqrt(z))*besseli(b - 1, sqrt(z)),
                 sqrt(z)*(besseli(-b, sqrt(z))*besseli(b - 1, sqrt(z))
                          + besseli(1 - b, sqrt(z))*besseli(b, sqrt(z))),
                 besseli(-b, sqrt(z))*besseli(b, sqrt(z))]),
         Matrix([[1, 0, 0]]),
         Matrix([[b - 1, S.Half, 0],
                 [z, 0, z],
                 [0, S.Half, -b]]))
    addb([S.Half], [Rational(3, 2), Rational(3, 2)],
         Matrix([Shi(2*sqrt(z))/2/sqrt(z), sinh(2*sqrt(z))/2/sqrt(z),
                 cosh(2*sqrt(z))]),
         Matrix([[1, 0, 0]]),
         Matrix([[Rational(-1, 2), S.Half, 0], [0, Rational(-1, 2), S.Half], [0, 2*z, 0]]))

    # FresnelS
    # Basic rule
    #add([Rational(3, 4)], [Rational(3, 2),Rational(7, 4)], 6*fresnels( exp(pi*I/4)*root(z,4)*2/sqrt(pi) ) / ( pi * (exp(pi*I/4)*root(z,4)*2/sqrt(pi))**3 ) )
    # Manually tuned rule
    addb([Rational(3, 4)], [Rational(3, 2), Rational(7, 4)],
         Matrix(
             [ fresnels(
                 exp(
                     pi*I/4)*root(
                         z, 4)*2/sqrt(
                             pi) ) / (
                                 pi * (exp(pi*I/4)*root(z, 4)*2/sqrt(pi))**3 ),
               sinh(2*sqrt(z))/sqrt(z),
               cosh(2*sqrt(z)) ]),
         Matrix([[6, 0, 0]]),
         Matrix([[Rational(-3, 4),  Rational(1, 16), 0],
                 [ 0,      Rational(-1, 2),  1],
                 [ 0,       z,       0]]))

    # FresnelC
    # Basic rule
    #add([Rational(1, 4)], [S.Half,Rational(5, 4)], fresnelc( exp(pi*I/4)*root(z,4)*2/sqrt(pi) ) / ( exp(pi*I/4)*root(z,4)*2/sqrt(pi) ) )
    # Manually tuned rule
    addb([Rational(1, 4)], [S.Half, Rational(5, 4)],
         Matrix(
             [ sqrt(
                 pi)*exp(
                     -I*pi/4)*fresnelc(
                         2*root(z, 4)*exp(I*pi/4)/sqrt(pi))/(2*root(z, 4)),
               cosh(2*sqrt(z)),
               sinh(2*sqrt(z))*sqrt(z) ]),
         Matrix([[1, 0, 0]]),
         Matrix([[Rational(-1, 4),  Rational(1, 4), 0     ],
                 [ 0,       0,      1     ],
                 [ 0,       z,      S.Half]]))

    # 2F3
    # XXX with this five-parameter formula is pretty slow with the current
    #     Formula.find_instantiations (creates 2!*3!*3**(2+3) ~ 3000
    #     instantiations ... But it's not too bad.
    addb([a, a + S.Half], [2*a, b, 2*a - b + 1],
         gamma(b)*gamma(2*a - b + 1) * (sqrt(z)/2)**(1 - 2*a) *
         Matrix([besseli(b - 1, sqrt(z))*besseli(2*a - b, sqrt(z)),
                 sqrt(z)*besseli(b, sqrt(z))*besseli(2*a - b, sqrt(z)),
                 sqrt(z)*besseli(b - 1, sqrt(z))*besseli(2*a - b + 1, sqrt(z)),
                 besseli(b, sqrt(z))*besseli(2*a - b + 1, sqrt(z))]),
         Matrix([[1, 0, 0, 0]]),
         Matrix([[0, S.Half, S.Half, 0],
                 [z/2, 1 - b, 0, z/2],
                 [z/2, 0, b - 2*a, z/2],
                 [0, S.Half, S.Half, -2*a]]))
    # (C/f above comment about eulergamma in the basis).
    addb([1, 1], [2, 2, Rational(3, 2)],
         Matrix([Chi(2*sqrt(z)) - log(2*sqrt(z)),
                 cosh(2*sqrt(z)), sqrt(z)*sinh(2*sqrt(z)), 1, EulerGamma]),
         Matrix([[1/z, 0, 0, 0, -1/z]]),
         Matrix([[0, S.Half, 0, Rational(-1, 2), 0],
                 [0, 0, 1, 0, 0],
                 [0, z, S.Half, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0]]))

    # 3F3
    # This is rule: https://functions.wolfram.com/07.31.03.0134.01
    # Initial reason to add it was a nice solution for
    # integrate(erf(a*z)/z**2, z) and same for erfc and erfi.
    # Basic rule
    # add([1, 1, a], [2, 2, a+1], (a/(z*(a-1)**2)) *
    #     (1 - (-z)**(1-a) * (gamma(a) - uppergamma(a,-z))
    #      - (a-1) * (EulerGamma + uppergamma(0,-z) + log(-z))
    #      - exp(z)))
    # Manually tuned rule
    addb([1, 1, a], [2, 2, a+1],
         Matrix([a*(log(-z) + expint(1, -z) + EulerGamma)/(z*(a**2 - 2*a + 1)),
                 a*(-z)**(-a)*(gamma(a) - uppergamma(a, -z))/(a - 1)**2,
                 a*exp(z)/(a**2 - 2*a + 1),
                 a/(z*(a**2 - 2*a + 1))]),
         Matrix([[1-a, 1, -1/z, 1]]),
         Matrix([[-1,0,-1/z,1],
                 [0,-a,1,0],
                 [0,0,z,0],
                 [0,0,0,-1]]))

