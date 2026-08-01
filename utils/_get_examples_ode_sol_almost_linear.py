
def _get_examples_ode_sol_almost_linear():
    from sympy.functions.special.error_functions import Ei
    A = Symbol('A', positive=True)
    f = Function('f')
    d = f(x).diff(x)

    return {
            'hint': "almost_linear",
            'func': f(x),
            'examples':{
    'almost_lin_01': {
        'eq': x**2*f(x)**2*d + f(x)**3 + 1,
        'sol': [Eq(f(x), (C1*exp(3/x) - 1)**Rational(1, 3)),
        Eq(f(x), (-1 - sqrt(3)*I)*(C1*exp(3/x) - 1)**Rational(1, 3)/2),
        Eq(f(x), (-1 + sqrt(3)*I)*(C1*exp(3/x) - 1)**Rational(1, 3)/2)],

    },

    'almost_lin_02': {
        'eq': x*f(x)*d + 2*x*f(x)**2 + 1,
        'sol': [Eq(f(x), -sqrt((C1 - 2*Ei(4*x))*exp(-4*x))), Eq(f(x), sqrt((C1 - 2*Ei(4*x))*exp(-4*x)))]
    },

    'almost_lin_03': {
        'eq':  x*d + x*f(x) + 1,
        'sol': [Eq(f(x), (C1 - Ei(x))*exp(-x))]
    },

    'almost_lin_04': {
        'eq': x*exp(f(x))*d + exp(f(x)) + 3*x,
        'sol': [Eq(f(x), log(C1/x - x*Rational(3, 2)))],
    },

    'almost_lin_05': {
        'eq': x + A*(x + diff(f(x), x) + f(x)) + diff(f(x), x) + f(x) + 2,
        'sol': [Eq(f(x), (C1 + Piecewise(
        (x, Eq(A + 1, 0)), ((-A*x + A - x - 1)*exp(x)/(A + 1), True)))*exp(-x))],
    },
    }
    }

