
def trig_substitution_rule(integral):
    integrand, symbol = integral
    A = Wild('a', exclude=[0, symbol])
    B = Wild('b', exclude=[0, symbol])
    theta = Dummy("theta")
    target_pattern = A + B*symbol**2

    matches = integrand.find(target_pattern)
    for expr in matches:
        match = expr.match(target_pattern)
        a = match.get(A, S.Zero)
        b = match.get(B, S.Zero)

        a_positive = ((a.is_number and a > 0) or a.is_positive)
        b_positive = ((b.is_number and b > 0) or b.is_positive)
        a_negative = ((a.is_number and a < 0) or a.is_negative)
        b_negative = ((b.is_number and b < 0) or b.is_negative)
        x_func = None
        if a_positive and b_positive:
            # a**2 + b*x**2. Assume sec(theta) > 0, -pi/2 < theta < pi/2
            x_func = (sqrt(a)/sqrt(b)) * tan(theta)
            # Do not restrict the domain: tan(theta) takes on any real
            # value on the interval -pi/2 < theta < pi/2 so x takes on
            # any value
            restriction = True
        elif a_positive and b_negative:
            # a**2 - b*x**2. Assume cos(theta) > 0, -pi/2 < theta < pi/2
            constant = sqrt(a)/sqrt(-b)
            x_func = constant * sin(theta)
            restriction = And(symbol > -constant, symbol < constant)
        elif a_negative and b_positive:
            # b*x**2 - a**2. Assume sin(theta) > 0, 0 < theta < pi
            constant = sqrt(-a)/sqrt(b)
            x_func = constant * sec(theta)
            restriction = And(symbol > -constant, symbol < constant)
        if x_func:
            # Manually simplify sqrt(trig(theta)**2) to trig(theta)
            # Valid due to assumed domain restriction
            substitutions = {}
            for f in [sin, cos, tan,
                      sec, csc, cot]:
                substitutions[sqrt(f(theta)**2)] = f(theta)
                substitutions[sqrt(f(theta)**(-2))] = 1/f(theta)

            replaced = integrand.subs(symbol, x_func).trigsimp()
            replaced = manual_subs(replaced, substitutions)
            if not replaced.has(symbol):
                replaced *= manual_diff(x_func, theta)
                replaced = replaced.trigsimp()
                secants = replaced.find(1/cos(theta))
                if secants:
                    replaced = replaced.xreplace({
                        1/cos(theta): sec(theta)
                    })

                substep = integral_steps(replaced, theta)
                if not substep.contains_dont_know():
                    return TrigSubstitutionRule(integrand, symbol,
                        theta, x_func, replaced, substep, restriction)

