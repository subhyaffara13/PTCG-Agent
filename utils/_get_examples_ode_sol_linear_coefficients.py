
def _get_examples_ode_sol_linear_coefficients():
    return {
            'hint': "linear_coefficients",
            'func': f(x),
            'examples':{
    'linear_coeff_01': {
        'eq': f(x).diff(x) + (3 + 2*f(x))/(x + 3),
        'sol': [Eq(f(x), C1/(x**2 + 6*x + 9) - Rational(3, 2))],
    },
    }
    }

