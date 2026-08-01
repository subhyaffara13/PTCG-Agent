
def _get_examples_ode_sol_2nd_nonlinear_autonomous_conserved():
    return {
            'hint': "2nd_nonlinear_autonomous_conserved",
            'func': f(x),
            'examples': {
    '2nd_nonlinear_autonomous_conserved_01': {
        'eq': f(x).diff(x, 2) + exp(f(x)) + log(f(x)),
        'sol': [
            Eq(Integral(1/sqrt(C1 - 2*_u*log(_u) + 2*_u - 2*exp(_u)), (_u, f(x))), C2 + x),
            Eq(Integral(1/sqrt(C1 - 2*_u*log(_u) + 2*_u - 2*exp(_u)), (_u, f(x))), C2 - x)
        ],
        'simplify_flag': False,
    },
    '2nd_nonlinear_autonomous_conserved_02': {
        'eq': f(x).diff(x, 2) + cbrt(f(x)) + 1/f(x),
        'sol': [
            Eq(sqrt(2)*Integral(1/sqrt(2*C1 - 3*_u**Rational(4, 3) - 4*log(_u)), (_u, f(x))), C2 + x),
            Eq(sqrt(2)*Integral(1/sqrt(2*C1 - 3*_u**Rational(4, 3) - 4*log(_u)), (_u, f(x))), C2 - x)
        ],
        'simplify_flag': False,
    },
    '2nd_nonlinear_autonomous_conserved_03': {
        'eq': f(x).diff(x, 2) + sin(f(x)),
        'sol': [
            Eq(Integral(1/sqrt(C1 + 2*cos(_u)), (_u, f(x))), C2 + x),
            Eq(Integral(1/sqrt(C1 + 2*cos(_u)), (_u, f(x))), C2 - x)
        ],
        'simplify_flag': False,
    },
    '2nd_nonlinear_autonomous_conserved_04': {
        'eq': f(x).diff(x, 2) + cosh(f(x)),
        'sol': [
            Eq(Integral(1/sqrt(C1 - 2*sinh(_u)), (_u, f(x))), C2 + x),
            Eq(Integral(1/sqrt(C1 - 2*sinh(_u)), (_u, f(x))), C2 - x)
        ],
        'simplify_flag': False,
    },
    '2nd_nonlinear_autonomous_conserved_05': {
        'eq': f(x).diff(x, 2) + asin(f(x)),
        'sol': [
            Eq(Integral(1/sqrt(C1 - 2*_u*asin(_u) - 2*sqrt(1 - _u**2)), (_u, f(x))), C2 + x),
            Eq(Integral(1/sqrt(C1 - 2*_u*asin(_u) - 2*sqrt(1 - _u**2)), (_u, f(x))), C2 - x)
        ],
        'simplify_flag': False,
        'XFAIL': ['2nd_nonlinear_autonomous_conserved_Integral']
    }
    }
    }

