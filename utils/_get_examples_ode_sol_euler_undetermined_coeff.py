
def _get_examples_ode_sol_euler_undetermined_coeff():
    return {
            'hint': "nth_linear_euler_eq_nonhomogeneous_undetermined_coefficients",
            'func': f(x),
            'examples':{
    'euler_undet_01': {
        'eq': Eq(x**2*diff(f(x), x, x) + x*diff(f(x), x), 1),
        'sol': [Eq(f(x), C1 + C2*log(x) + log(x)**2/2)]
    },

    'euler_undet_02': {
        'eq': Eq(x**2*diff(f(x), x, x) - 2*x*diff(f(x), x) + 2*f(x), x**3),
        'sol': [Eq(f(x), x*(C1 + C2*x + Rational(1, 2)*x**2))]
    },

    'euler_undet_03': {
        'eq': Eq(x**2*diff(f(x), x, x) - x*diff(f(x), x) - 3*f(x), log(x)/x),
        'sol': [Eq(f(x), (C1 + C2*x**4 - log(x)**2/8 - log(x)/16)/x)]
    },

    'euler_undet_04': {
        'eq': Eq(x**2*diff(f(x), x, x) + 3*x*diff(f(x), x) - 8*f(x), log(x)**3 - log(x)),
        'sol': [Eq(f(x), C1/x**4 + C2*x**2 - Rational(1,8)*log(x)**3 - Rational(3,32)*log(x)**2 - Rational(1,64)*log(x) - Rational(7, 256))]
    },

    'euler_undet_05': {
        'eq': Eq(x**3*diff(f(x), x, x, x) - 3*x**2*diff(f(x), x, x) + 6*x*diff(f(x), x) - 6*f(x), log(x)),
        'sol': [Eq(f(x), C1*x + C2*x**2 + C3*x**3 - Rational(1, 6)*log(x) - Rational(11, 36))]
    },

    #Below examples were added for the issue: https://github.com/sympy/sympy/issues/5096
    'euler_undet_06': {
        'eq': 2*x**2*f(x).diff(x, 2) + f(x) + sqrt(2*x)*sin(log(2*x)/2),
        'sol': [Eq(f(x), sqrt(x)*(C1*sin(log(x)/2) + C2*cos(log(x)/2) + sqrt(2)*log(x)*cos(log(2*x)/2)/2))]
    },

    'euler_undet_07': {
        'eq': 2*x**2*f(x).diff(x, 2) + f(x) + sin(log(2*x)/2),
        'sol': [Eq(f(x), C1*sqrt(x)*sin(log(x)/2) + C2*sqrt(x)*cos(log(x)/2) - 2*sin(log(2*x)/2)/5 - 4*cos(log(2*x)/2)/5)]
    },
    }
    }

