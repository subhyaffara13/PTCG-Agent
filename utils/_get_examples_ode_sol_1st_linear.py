
def _get_examples_ode_sol_1st_linear():
    # Type: first order linear form f'(x)+p(x)f(x)=q(x)
    return {
            'hint': "1st_linear",
            'func': f(x),
            'examples':{
    'linear_01': {
        'eq': Eq(f(x).diff(x) + x*f(x), x**2),
        'sol': [Eq(f(x), (C1 + x*exp(x**2/2)- sqrt(2)*sqrt(pi)*erfi(sqrt(2)*x/2)/2)*exp(-x**2/2))],
    },
    },
    }

