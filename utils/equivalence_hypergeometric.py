
def equivalence_hypergeometric(A, B, func):
    # This method for finding the equivalence is only for 2F1 type.
    # We can extend it for 1F1 and 0F1 type also.
    x = func.args[0]

    # making given equation in normal form
    I1 = factor(cancel(A.diff(x)/2 + A**2/4 - B))

    # computing shifted invariant(J1) of the equation
    J1 = factor(cancel(x**2*I1 + S(1)/4))
    num, dem = J1.as_numer_denom()
    num = powdenest(expand(num))
    dem = powdenest(expand(dem))
    # this function will compute the different powers of variable(x) in J1.
    # then it will help in finding value of k. k is power of x such that we can express
    # J1 = x**k * J0(x**k) then all the powers in J0 become integers.
    def _power_counting(num):
        _pow = {0}
        for val in num:
            if val.has(x):
                if isinstance(val, Pow) and val.as_base_exp()[0] == x:
                    _pow.add(val.as_base_exp()[1])
                elif val == x:
                    _pow.add(val.as_base_exp()[1])
                else:
                    _pow.update(_power_counting(val.args))
        return _pow

    pow_num = _power_counting((num, ))
    pow_dem = _power_counting((dem, ))
    pow_dem.update(pow_num)

    _pow = pow_dem
    k = gcd(_pow)

    # computing I0 of the given equation
    I0 = powdenest(simplify(factor(((J1/k**2) - S(1)/4)/((x**k)**2))), force=True)
    I0 = factor(cancel(powdenest(I0.subs(x, x**(S(1)/k)), force=True)))

    # Before this point I0, J1 might be functions of e.g. sqrt(x) but replacing
    # x with x**(1/k) should result in I0 being a rational function of x or
    # otherwise the hypergeometric solver cannot be used. Note that k can be a
    # non-integer rational such as 2/7.
    if not I0.is_rational_function(x):
        return None

    num, dem = I0.as_numer_denom()

    max_num_pow = max(_power_counting((num, )))
    dem_args = dem.args
    sing_point = []
    dem_pow = []
    # calculating singular point of I0.
    for arg in dem_args:
        if arg.has(x):
            if isinstance(arg, Pow):
                # (x-a)**n
                dem_pow.append(arg.as_base_exp()[1])
                sing_point.append(list(roots(arg.as_base_exp()[0], x).keys())[0])
            else:
                # (x-a) type
                dem_pow.append(arg.as_base_exp()[1])
                sing_point.append(list(roots(arg, x).keys())[0])

    dem_pow.sort()
    # checking if equivalence is exists or not.

    if equivalence(max_num_pow, dem_pow) == "2F1":
        return {'I0':I0, 'k':k, 'sing_point':sing_point, 'type':"2F1"}
    else:
        return None

