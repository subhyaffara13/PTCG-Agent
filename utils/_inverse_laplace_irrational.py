
def _inverse_laplace_irrational(fn, s, t, plane):
    """
    Helper function for the class InverseLaplaceTransform.
    """

    a = Wild('a', exclude=[s])
    b = Wild('b', exclude=[s])
    m = Wild('m', exclude=[s])
    n = Wild('n', exclude=[s])

    result = None
    condition = S.true

    fa = fn.as_ordered_factors()

    ma = [x.match((a*s**m+b)**n) for x in fa]

    if None in ma:
        return None

    constants = S.One
    zeros = []
    poles = []
    rest = []

    for term in ma:
        if term[a] == 0:
            constants = constants*term
        elif term[n].is_positive:
            zeros.append(term)
        elif term[n].is_negative:
            poles.append(term)
        else:
            rest.append(term)

    # The code below assumes that the poles are sorted in a specific way:
    poles = sorted(poles, key=lambda x: (x[n], x[b] != 0, x[b]))
    zeros = sorted(zeros, key=lambda x: (x[n], x[b] != 0, x[b]))

    if len(rest) != 0:
        return None

    if len(poles) == 1 and len(zeros) == 0:
        if poles[0][n] == -1 and poles[0][m] == S.Half:
            # 1/(a0*sqrt(s)+b0) == 1/a0 * 1/(sqrt(s)+b0/a0)
            a_ = poles[0][b]/poles[0][a]
            k_ = 1/poles[0][a]*constants
            if a_.is_positive:
                result = (
                    k_/sqrt(pi)/sqrt(t) -
                    k_*a_*exp(a_**2*t)*erfc(a_*sqrt(t)))
                _debug('     rule 5.3.4')
        elif poles[0][n] == -2 and poles[0][m] == S.Half:
            # 1/(a0*sqrt(s)+b0)**2 == 1/a0**2 * 1/(sqrt(s)+b0/a0)**2
            a_sq = poles[0][b]/poles[0][a]
            a_ = a_sq**2
            k_ = 1/poles[0][a]**2*constants
            if a_sq.is_positive:
                result = (
                    k_*(1 - 2/sqrt(pi)*sqrt(a_)*sqrt(t) +
                        (1-2*a_*t)*exp(a_*t)*(erf(sqrt(a_)*sqrt(t))-1)))
                _debug('     rule 5.3.10')
        elif poles[0][n] == -3 and poles[0][m] == S.Half:
            # 1/(a0*sqrt(s)+b0)**3 == 1/a0**3 * 1/(sqrt(s)+b0/a0)**3
            a_ = poles[0][b]/poles[0][a]
            k_ = 1/poles[0][a]**3*constants
            if a_.is_positive:
                result = (
                    k_*(2/sqrt(pi)*(a_**2*t+1)*sqrt(t) -
                        a_*t*exp(a_**2*t)*(2*a_**2*t+3)*erfc(a_*sqrt(t))))
                _debug('     rule 5.3.13')
        elif poles[0][n] == -4 and poles[0][m] == S.Half:
            # 1/(a0*sqrt(s)+b0)**4 == 1/a0**4 * 1/(sqrt(s)+b0/a0)**4
            a_ = poles[0][b]/poles[0][a]
            k_ = 1/poles[0][a]**4*constants/3
            if a_.is_positive:
                result = (
                    k_*(t*(4*a_**4*t**2+12*a_**2*t+3)*exp(a_**2*t) *
                        erfc(a_*sqrt(t)) -
                        2/sqrt(pi)*a_**3*t**(S(5)/2)*(2*a_**2*t+5)))
                _debug('     rule 5.3.16')
        elif poles[0][n] == -S.Half and poles[0][m] == 2:
            # 1/sqrt(a0*s**2+b0) == 1/sqrt(a0) * 1/sqrt(s**2+b0/a0)
            a_ = sqrt(poles[0][b]/poles[0][a])
            k_ = 1/sqrt(poles[0][a])*constants
            result = (k_*(besselj(0, a_*t)))
            _debug('     rule 5.3.35/44')

    elif len(poles) == 1 and len(zeros) == 1:
        if (
                poles[0][n] == -3 and poles[0][m] == S.Half and
                zeros[0][n] == S.Half and zeros[0][b] == 0):
            # sqrt(az*s)/(ap*sqrt(s+bp)**3)
            # == sqrt(az)/ap * sqrt(s)/(sqrt(s+bp)**3)
            a_ = poles[0][b]
            k_ = sqrt(zeros[0][a])/poles[0][a]*constants
            result = (
                k_*(2*a_**4*t**2+5*a_**2*t+1)*exp(a_**2*t) *
                erfc(a_*sqrt(t)) - 2/sqrt(pi)*a_*(a_**2*t+2)*sqrt(t))
            _debug('     rule 5.3.14')
        if (
                poles[0][n] == -1 and poles[0][m] == 1 and
                zeros[0][n] == S.Half and zeros[0][m] == 1):
            # sqrt(az*s+bz)/(ap*s+bp)
            # == sqrt(az)/ap * (sqrt(s+bz/az)/(s+bp/ap))
            a_ = zeros[0][b]/zeros[0][a]
            b_ = poles[0][b]/poles[0][a]
            k_ = sqrt(zeros[0][a])/poles[0][a]*constants
            result = (
                k_*(exp(-a_*t)/sqrt(t)/sqrt(pi)+sqrt(a_-b_) *
                    exp(-b_*t)*erf(sqrt(a_-b_)*sqrt(t))))
            _debug('     rule 5.3.22')

    elif len(poles) == 2 and len(zeros) == 0:
        if (
                poles[0][n] == -1 and poles[0][m] == 1 and
                poles[1][n] == -S.Half and poles[1][m] == 1 and
                poles[1][b] == 0):
            # 1/((a0*s+b0)*sqrt(a1*s))
            # == 1/(a0*sqrt(a1)) * 1/((s+b0/a0)*sqrt(s))
            a_ = -poles[0][b]/poles[0][a]
            k_ = 1/sqrt(poles[1][a])/poles[0][a]*constants
            if a_.is_positive:
                result = (k_/sqrt(a_)*exp(a_*t)*erf(sqrt(a_)*sqrt(t)))
                _debug('     rule 5.3.1')
        elif (
                poles[0][n] == -1 and poles[0][m] == 1 and poles[0][b] == 0 and
                poles[1][n] == -1 and poles[1][m] == S.Half):
            # 1/(a0*s*(a1*sqrt(s)+b1))
            # == 1/(a0*a1) * 1/(s*(sqrt(s)+b1/a1))
            a_ = poles[1][b]/poles[1][a]
            k_ = 1/poles[0][a]/poles[1][a]/a_*constants
            if a_.is_positive:
                result = k_*(1-exp(a_**2*t)*erfc(a_*sqrt(t)))
                _debug('     rule 5.3.5')
        elif (
                poles[0][n] == -1 and poles[0][m] == S.Half and
                poles[1][n] == -S.Half and poles[1][m] == 1 and
                poles[1][b] == 0):
            # 1/((a0*sqrt(s)+b0)*(sqrt(a1*s))
            # == 1/(a0*sqrt(a1)) * 1/((sqrt(s)+b0/a0)"sqrt(s))
            a_ = poles[0][b]/poles[0][a]
            k_ = 1/(poles[0][a]*sqrt(poles[1][a]))*constants
            if a_.is_positive:
                result = k_*exp(a_**2*t)*erfc(a_*sqrt(t))
                _debug('     rule 5.3.7')
        elif (
                poles[0][n] == -S(3)/2 and poles[0][m] == 1 and
                poles[0][b] == 0 and poles[1][n] == -1 and
                poles[1][m] == S.Half):
            # 1/((a0**(3/2)*s**(3/2))*(a1*sqrt(s)+b1))
            # == 1/(a0**(3/2)*a1)  1/((s**(3/2))*(sqrt(s)+b1/a1))
            # Note that Bateman54 5.3 (8) is incorrect; there (sqrt(p)+a)
            # should be (sqrt(p)+a)**(-1).
            a_ = poles[1][b]/poles[1][a]
            k_ = 1/(poles[0][a]**(S(3)/2)*poles[1][a])/a_**2*constants
            if a_.is_positive:
                result = (
                    k_*(2/sqrt(pi)*a_*sqrt(t)+exp(a_**2*t)*erfc(a_*sqrt(t))-1))
                _debug('     rule 5.3.8')
        elif (
                poles[0][n] == -2 and poles[0][m] == S.Half and
                poles[1][n] == -1 and poles[1][m] == 1 and
                poles[1][b] == 0):
            # 1/((a0*sqrt(s)+b0)**2*a1*s)
            # == 1/a0**2/a1 * 1/(sqrt(s)+b0/a0)**2/s
            a_sq = poles[0][b]/poles[0][a]
            a_ = a_sq**2
            k_ = 1/poles[0][a]**2/poles[1][a]*constants
            if a_sq.is_positive:
                result = (
                    k_*(1/a_ + (2*t-1/a_)*exp(a_*t)*erfc(sqrt(a_)*sqrt(t)) -
                        2/sqrt(pi)/sqrt(a_)*sqrt(t)))
                _debug('     rule 5.3.11')
        elif (
                poles[0][n] == -2 and poles[0][m] == S.Half and
                poles[1][n] == -S.Half and poles[1][m] == 1 and
                poles[1][b] == 0):
            # 1/((a0*sqrt(s)+b0)**2*sqrt(a1*s))
            # == 1/a0**2/sqrt(a1) * 1/(sqrt(s)+b0/a0)**2/sqrt(s)
            a_ = poles[0][b]/poles[0][a]
            k_ = 1/poles[0][a]**2/sqrt(poles[1][a])*constants
            if a_.is_positive:
                result = (
                    k_*(2/sqrt(pi)*sqrt(t) -
                        2*a_*t*exp(a_**2*t)*erfc(a_*sqrt(t))))
                _debug('     rule 5.3.12')
        elif (
                poles[0][n] == -3 and poles[0][m] == S.Half and
                poles[1][n] == -S.Half and poles[1][m] == 1 and
                poles[1][b] == 0):
            # 1 / (sqrt(a1*s)*(a0*sqrt(s+b0)**3))
            # == 1/(sqrt(a1)*a0) * 1/(sqrt(s)*(sqrt(s+b0)**3))
            a_ = poles[0][b]
            k_ = constants/sqrt(poles[1][a])/poles[0][a]
            result = k_*(
                (2*a_**2*t+1)*t*exp(a_**2*t)*erfc(a_*sqrt(t)) -
                2/sqrt(pi)*a_*t**(S(3)/2))
            _debug('     rule 5.3.15')
        elif (
                poles[0][n] == -1 and poles[0][m] == 1 and
                poles[1][n] == -S.Half and poles[1][m] == 1):
            # 1 / ( (a0*s+b0)* sqrt(a1*s+b1) )
            # == 1/(sqrt(a1)*a0) * 1 / ( (s+b0/a0)* sqrt(s+b1/a1) )
            a_ = poles[0][b]/poles[0][a]
            b_ = poles[1][b]/poles[1][a]
            k_ = constants/sqrt(poles[1][a])/poles[0][a]
            result = k_*(
                1/sqrt(b_-a_)*exp(-a_*t)*erf(sqrt(b_-a_)*sqrt(t)))
            _debug('     rule 5.3.23')

    elif len(poles) == 2 and len(zeros) == 1:
        if (
                poles[0][n] == -1 and poles[0][m] == 1 and
                poles[1][n] == -1 and poles[1][m] == S.Half and
                zeros[0][n] == S.Half and zeros[0][m] == 1 and
                zeros[0][b] == 0):
            # sqrt(za0*s)/((a0*s+b0)*(a1*sqrt(s)+b1))
            # == sqrt(za0)/(a0*a1) * s/((s+b0/a0)*(sqrt(s)+b1/a1))
            a_sq = poles[1][b]/poles[1][a]
            a_ = a_sq**2
            b_ = -poles[0][b]/poles[0][a]
            k_ = sqrt(zeros[0][a])/poles[0][a]/poles[1][a]/(a_-b_)*constants
            if a_sq.is_positive and b_.is_positive:
                result = k_*(
                    a_*exp(a_*t)*erfc(sqrt(a_)*sqrt(t)) +
                    sqrt(a_)*sqrt(b_)*exp(b_*t)*erfc(sqrt(b_)*sqrt(t)) -
                    b_*exp(b_*t))
                _debug('     rule 5.3.6')
        elif (
                poles[0][n] == -1 and poles[0][m] == 1 and
                poles[0][b] == 0 and poles[1][n] == -1 and
                poles[1][m] == S.Half and zeros[0][n] == 1 and
                zeros[0][m] == S.Half):
            # (az*sqrt(s)+bz)/(a0*s*(a1*sqrt(s)+b1))
            # == az/a0/a1 * (sqrt(z)+bz/az)/(s*(sqrt(s)+b1/a1))
            a_num = zeros[0][b]/zeros[0][a]
            a_ = poles[1][b]/poles[1][a]
            if a_+a_num == 0:
                k_ = zeros[0][a]/poles[0][a]/poles[1][a]*constants
                result = k_*(
                    2*exp(a_**2*t)*erfc(a_*sqrt(t))-1)
                _debug('     rule 5.3.17')
        elif (
                poles[1][n] == -1 and poles[1][m] == 1 and
                poles[1][b] == 0 and poles[0][n] == -2 and
                poles[0][m] == S.Half and zeros[0][n] == 2 and
                zeros[0][m] == S.Half):
            # (az*sqrt(s)+bz)**2/(a1*s*(a0*sqrt(s)+b0)**2)
            # == az**2/a1/a0**2 * (sqrt(z)+bz/az)**2/(s*(sqrt(s)+b0/a0)**2)
            a_num = zeros[0][b]/zeros[0][a]
            a_ = poles[0][b]/poles[0][a]
            if a_+a_num == 0:
                k_ = zeros[0][a]**2/poles[1][a]/poles[0][a]**2*constants
                result = k_*(
                    1 + 8*a_**2*t*exp(a_**2*t)*erfc(a_*sqrt(t)) -
                    8/sqrt(pi)*a_*sqrt(t))
                _debug('     rule 5.3.18')
        elif (
                poles[1][n] == -1 and poles[1][m] == 1 and
                poles[1][b] == 0 and poles[0][n] == -3 and
                poles[0][m] == S.Half and zeros[0][n] == 3 and
                zeros[0][m] == S.Half):
            # (az*sqrt(s)+bz)**3/(a1*s*(a0*sqrt(s)+b0)**3)
            # == az**3/a1/a0**3 * (sqrt(z)+bz/az)**3/(s*(sqrt(s)+b0/a0)**3)
            a_num = zeros[0][b]/zeros[0][a]
            a_ = poles[0][b]/poles[0][a]
            if a_+a_num == 0:
                k_ = zeros[0][a]**3/poles[1][a]/poles[0][a]**3*constants
                result = k_*(
                    2*(8*a_**4*t**2+8*a_**2*t+1)*exp(a_**2*t) *
                    erfc(a_*sqrt(t))-8/sqrt(pi)*a_*sqrt(t)*(2*a_**2*t+1)-1)
                _debug('     rule 5.3.19')

    elif len(poles) == 3 and len(zeros) == 0:
        if (
                poles[0][n] == -1 and poles[0][b] == 0 and poles[0][m] == 1 and
                poles[1][n] == -1 and poles[1][m] == 1 and
                poles[2][n] == -S.Half and poles[2][m] == 1):
            # 1/((a0*s)*(a1*s+b1)*sqrt(a2*s))
            # == 1/(a0*a1*sqrt(a2)) * 1/((s)*(s+b1/a1)*sqrt(s))
            a_ = -poles[1][b]/poles[1][a]
            k_ = 1/poles[0][a]/poles[1][a]/sqrt(poles[2][a])*constants
            if a_.is_positive:
                result = k_ * (
                    a_**(-S(3)/2) * exp(a_*t) * erf(sqrt(a_)*sqrt(t)) -
                    2/a_/sqrt(pi)*sqrt(t))
                _debug('     rule 5.3.2')
        elif (
                poles[0][n] == -1 and poles[0][m] == 1 and
                poles[1][n] == -1 and poles[1][m] == S.Half and
                poles[2][n] == -S.Half and poles[2][m] == 1 and
                poles[2][b] == 0):
            # 1/((a0*s+b0)*(a1*sqrt(s)+b1)*(sqrt(a2)*sqrt(s)))
            # == 1/(a0*a1*sqrt(a2)) * 1/((s+b0/a0)*(sqrt(s)+b1/a1)*sqrt(s))
            a_sq = poles[1][b]/poles[1][a]
            a_ = a_sq**2
            b_ = -poles[0][b]/poles[0][a]
            k_ = (
                1/poles[0][a]/poles[1][a]/sqrt(poles[2][a]) /
                (sqrt(b_)*(a_-b_)))
            if a_sq.is_positive and b_.is_positive:
                result = k_ * (
                    sqrt(b_)*exp(a_*t)*erfc(sqrt(a_)*sqrt(t)) +
                    sqrt(a_)*exp(b_*t)*erf(sqrt(b_)*sqrt(t)) -
                    sqrt(b_)*exp(b_*t))
                _debug('     rule 5.3.9')

    if result is None:
        return None
    else:
        return Heaviside(t)*result, condition

