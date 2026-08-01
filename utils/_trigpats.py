
def _trigpats():
    global _trigpat
    a, b, c = symbols('a b c', cls=Wild)
    d = Wild('d', commutative=False)

    # for the simplifications like sinh/cosh -> tanh:
    # DO NOT REORDER THE FIRST 14 since these are assumed to be in this
    # order in _match_div_rewrite.
    matchers_division = (
        (a*sin(b)**c/cos(b)**c, a*tan(b)**c, sin(b), cos(b)),
        (a*tan(b)**c*cos(b)**c, a*sin(b)**c, sin(b), cos(b)),
        (a*cot(b)**c*sin(b)**c, a*cos(b)**c, sin(b), cos(b)),
        (a*tan(b)**c/sin(b)**c, a/cos(b)**c, sin(b), cos(b)),
        (a*cot(b)**c/cos(b)**c, a/sin(b)**c, sin(b), cos(b)),
        (a*cot(b)**c*tan(b)**c, a, sin(b), cos(b)),
        (a*(cos(b) + 1)**c*(cos(b) - 1)**c,
            a*(-sin(b)**2)**c, cos(b) + 1, cos(b) - 1),
        (a*(sin(b) + 1)**c*(sin(b) - 1)**c,
            a*(-cos(b)**2)**c, sin(b) + 1, sin(b) - 1),

        (a*sinh(b)**c/cosh(b)**c, a*tanh(b)**c, S.One, S.One),
        (a*tanh(b)**c*cosh(b)**c, a*sinh(b)**c, S.One, S.One),
        (a*coth(b)**c*sinh(b)**c, a*cosh(b)**c, S.One, S.One),
        (a*tanh(b)**c/sinh(b)**c, a/cosh(b)**c, S.One, S.One),
        (a*coth(b)**c/cosh(b)**c, a/sinh(b)**c, S.One, S.One),
        (a*coth(b)**c*tanh(b)**c, a, S.One, S.One),

        (c*(tanh(a) + tanh(b))/(1 + tanh(a)*tanh(b)),
            tanh(a + b)*c, S.One, S.One),
    )

    matchers_add = (
        (c*sin(a)*cos(b) + c*cos(a)*sin(b) + d, sin(a + b)*c + d),
        (c*cos(a)*cos(b) - c*sin(a)*sin(b) + d, cos(a + b)*c + d),
        (c*sin(a)*cos(b) - c*cos(a)*sin(b) + d, sin(a - b)*c + d),
        (c*cos(a)*cos(b) + c*sin(a)*sin(b) + d, cos(a - b)*c + d),
        (c*sinh(a)*cosh(b) + c*sinh(b)*cosh(a) + d, sinh(a + b)*c + d),
        (c*cosh(a)*cosh(b) + c*sinh(a)*sinh(b) + d, cosh(a + b)*c + d),
    )

    # for cos(x)**2 + sin(x)**2 -> 1
    matchers_identity = (
        (a*sin(b)**2, a - a*cos(b)**2),
        (a*tan(b)**2, a*(1/cos(b))**2 - a),
        (a*cot(b)**2, a*(1/sin(b))**2 - a),
        (a*sin(b + c), a*(sin(b)*cos(c) + sin(c)*cos(b))),
        (a*cos(b + c), a*(cos(b)*cos(c) - sin(b)*sin(c))),
        (a*tan(b + c), a*((tan(b) + tan(c))/(1 - tan(b)*tan(c)))),

        (a*sinh(b)**2, a*cosh(b)**2 - a),
        (a*tanh(b)**2, a - a*(1/cosh(b))**2),
        (a*coth(b)**2, a + a*(1/sinh(b))**2),
        (a*sinh(b + c), a*(sinh(b)*cosh(c) + sinh(c)*cosh(b))),
        (a*cosh(b + c), a*(cosh(b)*cosh(c) + sinh(b)*sinh(c))),
        (a*tanh(b + c), a*((tanh(b) + tanh(c))/(1 + tanh(b)*tanh(c)))),

    )

    # Reduce any lingering artifacts, such as sin(x)**2 changing
    # to 1-cos(x)**2 when sin(x)**2 was "simpler"
    artifacts = (
        (a - a*cos(b)**2 + c, a*sin(b)**2 + c, cos),
        (a - a*(1/cos(b))**2 + c, -a*tan(b)**2 + c, cos),
        (a - a*(1/sin(b))**2 + c, -a*cot(b)**2 + c, sin),

        (a - a*cosh(b)**2 + c, -a*sinh(b)**2 + c, cosh),
        (a - a*(1/cosh(b))**2 + c, a*tanh(b)**2 + c, cosh),
        (a + a*(1/sinh(b))**2 + c, a*coth(b)**2 + c, sinh),

        # same as above but with noncommutative prefactor
        (a*d - a*d*cos(b)**2 + c, a*d*sin(b)**2 + c, cos),
        (a*d - a*d*(1/cos(b))**2 + c, -a*d*tan(b)**2 + c, cos),
        (a*d - a*d*(1/sin(b))**2 + c, -a*d*cot(b)**2 + c, sin),

        (a*d - a*d*cosh(b)**2 + c, -a*d*sinh(b)**2 + c, cosh),
        (a*d - a*d*(1/cosh(b))**2 + c, a*d*tanh(b)**2 + c, cosh),
        (a*d + a*d*(1/sinh(b))**2 + c, a*d*coth(b)**2 + c, sinh),
    )

    _trigpat = (a, b, c, d, matchers_division, matchers_add,
        matchers_identity, artifacts)
    return _trigpat

