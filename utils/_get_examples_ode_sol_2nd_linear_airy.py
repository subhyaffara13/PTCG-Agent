
def _get_examples_ode_sol_2nd_linear_airy():
    return {
            'hint': "2nd_linear_airy",
            'func': f(x),
            'examples':{
    '2nd_lin_airy_01': {
        'eq': f(x).diff(x, 2) - x*f(x),
        'sol': [Eq(f(x), C1*airyai(x) + C2*airybi(x))],
    },

    '2nd_lin_airy_02': {
        'eq': f(x).diff(x, 2) + 2*x*f(x),
        'sol': [Eq(f(x), C1*airyai(-2**(S(1)/3)*x) + C2*airybi(-2**(S(1)/3)*x))],
    },
    }
    }

