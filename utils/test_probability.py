
def test_probability():
    # various integrals from probability theory
    from sympy.core.function import expand_mul
    from sympy.core.symbol import (Symbol, symbols)
    from sympy.simplify.gammasimp import gammasimp
    from sympy.simplify.powsimp import powsimp
    mu1, mu2 = symbols('mu1 mu2', nonzero=True)
    sigma1, sigma2 = symbols('sigma1 sigma2', positive=True)
    rate = Symbol('lambda', positive=True)

    def normal(x, mu, sigma):
        return 1/sqrt(2*pi*sigma**2)*exp(-(x - mu)**2/2/sigma**2)

    def exponential(x, rate):
        return rate*exp(-rate*x)

    assert integrate(normal(x, mu1, sigma1), (x, -oo, oo), meijerg=True) == 1
    assert integrate(x*normal(x, mu1, sigma1), (x, -oo, oo), meijerg=True) == \
        mu1
    assert integrate(x**2*normal(x, mu1, sigma1), (x, -oo, oo), meijerg=True) \
        == mu1**2 + sigma1**2
    assert integrate(x**3*normal(x, mu1, sigma1), (x, -oo, oo), meijerg=True) \
        == mu1**3 + 3*mu1*sigma1**2
    assert integrate(normal(x, mu1, sigma1)*normal(y, mu2, sigma2),
                     (x, -oo, oo), (y, -oo, oo), meijerg=True) == 1
    assert integrate(x*normal(x, mu1, sigma1)*normal(y, mu2, sigma2),
                     (x, -oo, oo), (y, -oo, oo), meijerg=True) == mu1
    assert integrate(y*normal(x, mu1, sigma1)*normal(y, mu2, sigma2),
                     (x, -oo, oo), (y, -oo, oo), meijerg=True) == mu2
    assert integrate(x*y*normal(x, mu1, sigma1)*normal(y, mu2, sigma2),
                     (x, -oo, oo), (y, -oo, oo), meijerg=True) == mu1*mu2
    assert integrate((x + y + 1)*normal(x, mu1, sigma1)*normal(y, mu2, sigma2),
                     (x, -oo, oo), (y, -oo, oo), meijerg=True) == 1 + mu1 + mu2
    assert integrate((x + y - 1)*normal(x, mu1, sigma1)*normal(y, mu2, sigma2),
                     (x, -oo, oo), (y, -oo, oo), meijerg=True) == \
        -1 + mu1 + mu2

    i = integrate(x**2*normal(x, mu1, sigma1)*normal(y, mu2, sigma2),
                  (x, -oo, oo), (y, -oo, oo), meijerg=True)
    assert not i.has(Abs)
    assert simplify(i) == mu1**2 + sigma1**2
    assert integrate(y**2*normal(x, mu1, sigma1)*normal(y, mu2, sigma2),
                     (x, -oo, oo), (y, -oo, oo), meijerg=True) == \
        sigma2**2 + mu2**2

    assert integrate(exponential(x, rate), (x, 0, oo), meijerg=True) == 1
    assert integrate(x*exponential(x, rate), (x, 0, oo), meijerg=True) == \
        1/rate
    assert integrate(x**2*exponential(x, rate), (x, 0, oo), meijerg=True) == \
        2/rate**2

    def E(expr):
        res1 = integrate(expr*exponential(x, rate)*normal(y, mu1, sigma1),
                         (x, 0, oo), (y, -oo, oo), meijerg=True)
        res2 = integrate(expr*exponential(x, rate)*normal(y, mu1, sigma1),
                        (y, -oo, oo), (x, 0, oo), meijerg=True)
        assert expand_mul(res1) == expand_mul(res2)
        return res1

    assert E(1) == 1
    assert E(x*y) == mu1/rate
    assert E(x*y**2) == mu1**2/rate + sigma1**2/rate
    ans = sigma1**2 + 1/rate**2
    assert simplify(E((x + y + 1)**2) - E(x + y + 1)**2) == ans
    assert simplify(E((x + y - 1)**2) - E(x + y - 1)**2) == ans
    assert simplify(E((x + y)**2) - E(x + y)**2) == ans

    # Beta' distribution
    alpha, beta = symbols('alpha beta', positive=True)
    betadist = x**(alpha - 1)*(1 + x)**(-alpha - beta)*gamma(alpha + beta) \
        /gamma(alpha)/gamma(beta)
    assert integrate(betadist, (x, 0, oo), meijerg=True) == 1
    i = integrate(x*betadist, (x, 0, oo), meijerg=True, conds='separate')
    assert (gammasimp(i[0]), i[1]) == (alpha/(beta - 1), 1 < beta)
    j = integrate(x**2*betadist, (x, 0, oo), meijerg=True, conds='separate')
    assert j[1] == (beta > 2)
    assert gammasimp(j[0] - i[0]**2) == (alpha + beta - 1)*alpha \
        /(beta - 2)/(beta - 1)**2

    # Beta distribution
    # NOTE: this is evaluated using antiderivatives. It also tests that
    #       meijerint_indefinite returns the simplest possible answer.
    a, b = symbols('a b', positive=True)
    betadist = x**(a - 1)*(-x + 1)**(b - 1)*gamma(a + b)/(gamma(a)*gamma(b))
    assert simplify(integrate(betadist, (x, 0, 1), meijerg=True)) == 1
    assert simplify(integrate(x*betadist, (x, 0, 1), meijerg=True)) == \
        a/(a + b)
    assert simplify(integrate(x**2*betadist, (x, 0, 1), meijerg=True)) == \
        a*(a + 1)/(a + b)/(a + b + 1)
    assert simplify(integrate(x**y*betadist, (x, 0, 1), meijerg=True)) == \
        gamma(a + b)*gamma(a + y)/gamma(a)/gamma(a + b + y)

    # Chi distribution
    k = Symbol('k', integer=True, positive=True)
    chi = 2**(1 - k/2)*x**(k - 1)*exp(-x**2/2)/gamma(k/2)
    assert powsimp(integrate(chi, (x, 0, oo), meijerg=True)) == 1
    assert simplify(integrate(x*chi, (x, 0, oo), meijerg=True)) == \
        sqrt(2)*gamma((k + 1)/2)/gamma(k/2)
    assert simplify(integrate(x**2*chi, (x, 0, oo), meijerg=True)) == k

    # Chi^2 distribution
    chisquared = 2**(-k/2)/gamma(k/2)*x**(k/2 - 1)*exp(-x/2)
    assert powsimp(integrate(chisquared, (x, 0, oo), meijerg=True)) == 1
    assert simplify(integrate(x*chisquared, (x, 0, oo), meijerg=True)) == k
    assert simplify(integrate(x**2*chisquared, (x, 0, oo), meijerg=True)) == \
        k*(k + 2)
    assert gammasimp(integrate(((x - k)/sqrt(2*k))**3*chisquared, (x, 0, oo),
                    meijerg=True)) == 2*sqrt(2)/sqrt(k)

    # Dagum distribution
    a, b, p = symbols('a b p', positive=True)
    # XXX (x/b)**a does not work
    dagum = a*p/x*(x/b)**(a*p)/(1 + x**a/b**a)**(p + 1)
    assert simplify(integrate(dagum, (x, 0, oo), meijerg=True)) == 1
    # XXX conditions are a mess
    arg = x*dagum
    assert simplify(integrate(arg, (x, 0, oo), meijerg=True, conds='none')
                    ) == a*b*gamma(1 - 1/a)*gamma(p + 1 + 1/a)/(
                    (a*p + 1)*gamma(p))
    assert simplify(integrate(x*arg, (x, 0, oo), meijerg=True, conds='none')
                    ) == a*b**2*gamma(1 - 2/a)*gamma(p + 1 + 2/a)/(
                    (a*p + 2)*gamma(p))

    # F-distribution
    d1, d2 = symbols('d1 d2', positive=True)
    f = sqrt(((d1*x)**d1 * d2**d2)/(d1*x + d2)**(d1 + d2))/x \
        /gamma(d1/2)/gamma(d2/2)*gamma((d1 + d2)/2)
    assert simplify(integrate(f, (x, 0, oo), meijerg=True)) == 1
    # TODO conditions are a mess
    assert simplify(integrate(x*f, (x, 0, oo), meijerg=True, conds='none')
                    ) == d2/(d2 - 2)
    assert simplify(integrate(x**2*f, (x, 0, oo), meijerg=True, conds='none')
                    ) == d2**2*(d1 + 2)/d1/(d2 - 4)/(d2 - 2)

    # TODO gamma, rayleigh

    # inverse gaussian
    lamda, mu = symbols('lamda mu', positive=True)
    dist = sqrt(lamda/2/pi)*x**(Rational(-3, 2))*exp(-lamda*(x - mu)**2/x/2/mu**2)
    mysimp = lambda expr: simplify(expr.rewrite(exp))
    assert mysimp(integrate(dist, (x, 0, oo))) == 1
    assert mysimp(integrate(x*dist, (x, 0, oo))) == mu
    assert mysimp(integrate((x - mu)**2*dist, (x, 0, oo))) == mu**3/lamda
    assert mysimp(integrate((x - mu)**3*dist, (x, 0, oo))) == 3*mu**5/lamda**2

    # Levi
    c = Symbol('c', positive=True)
    assert integrate(sqrt(c/2/pi)*exp(-c/2/(x - mu))/(x - mu)**S('3/2'),
                    (x, mu, oo)) == 1
    # higher moments oo

    # log-logistic
    alpha, beta = symbols('alpha beta', positive=True)
    distn = (beta/alpha)*x**(beta - 1)/alpha**(beta - 1)/ \
        (1 + x**beta/alpha**beta)**2
    # FIXME: If alpha, beta are not declared as finite the line below hangs
    # after the changes in:
    #    https://github.com/sympy/sympy/pull/16603
    assert simplify(integrate(distn, (x, 0, oo))) == 1
    # NOTE the conditions are a mess, but correctly state beta > 1
    assert simplify(integrate(x*distn, (x, 0, oo), conds='none')) == \
        pi*alpha/beta/sin(pi/beta)
    # (similar comment for conditions applies)
    assert simplify(integrate(x**y*distn, (x, 0, oo), conds='none')) == \
        pi*alpha**y*y/beta/sin(pi*y/beta)

    # weibull
    k = Symbol('k', positive=True)
    n = Symbol('n', positive=True)
    distn = k/lamda*(x/lamda)**(k - 1)*exp(-(x/lamda)**k)
    assert simplify(integrate(distn, (x, 0, oo))) == 1
    assert simplify(integrate(x**n*distn, (x, 0, oo))) == \
        lamda**n*gamma(1 + n/k)

    # rice distribution
    from sympy.functions.special.bessel import besseli
    nu, sigma = symbols('nu sigma', positive=True)
    rice = x/sigma**2*exp(-(x**2 + nu**2)/2/sigma**2)*besseli(0, x*nu/sigma**2)
    assert integrate(rice, (x, 0, oo), meijerg=True) == 1
    # can someone verify higher moments?

    # Laplace distribution
    mu = Symbol('mu', real=True)
    b = Symbol('b', positive=True)
    laplace = exp(-abs(x - mu)/b)/2/b
    assert integrate(laplace, (x, -oo, oo), meijerg=True) == 1
    assert integrate(x*laplace, (x, -oo, oo), meijerg=True) == mu
    assert integrate(x**2*laplace, (x, -oo, oo), meijerg=True) == \
        2*b**2 + mu**2

    # TODO are there other distributions supported on (-oo, oo) that we can do?

    # misc tests
    k = Symbol('k', positive=True)
    assert gammasimp(expand_mul(integrate(log(x)*x**(k - 1)*exp(-x)/gamma(k),
                              (x, 0, oo)))) == polygamma(0, k)

