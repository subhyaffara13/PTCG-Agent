
def _get_examples_ode_sol_nth_order_reducible():
    return {
            'hint': "nth_order_reducible",
            'func': f(x),
            'examples':{
    'reducible_01': {
        'eq': Eq(x*Derivative(f(x), x)**2 + Derivative(f(x), x, 2), 0),
        'sol': [Eq(f(x),C1 - sqrt(-1/C2)*log(-C2*sqrt(-1/C2) + x) +
        sqrt(-1/C2)*log(C2*sqrt(-1/C2) + x))],
        'slow': True,
    },

    'reducible_02': {
        'eq': -exp(x) + (x*Derivative(f(x), (x, 2)) + Derivative(f(x), x))/x,
        'sol': [Eq(f(x), C1 + C2*log(x) + exp(x) - Ei(x))],
        'slow': True,
    },

    'reducible_03': {
        'eq': Eq(sqrt(2) * f(x).diff(x,x,x) + f(x).diff(x), 0),
        'sol': [Eq(f(x), C1 + C2*sin(2**Rational(3, 4)*x/2) + C3*cos(2**Rational(3, 4)*x/2))],
        'slow': True,
    },

    'reducible_04': {
        'eq': f(x).diff(x, 2) + 2*f(x).diff(x),
        'sol': [Eq(f(x), C1 + C2*exp(-2*x))],
    },

    'reducible_05': {
        'eq': f(x).diff(x, 3) + f(x).diff(x, 2) - 6*f(x).diff(x),
        'sol': [Eq(f(x), C1 + C2*exp(-3*x) + C3*exp(2*x))],
        'slow': True,
    },

    'reducible_06': {
        'eq': f(x).diff(x, 4) - f(x).diff(x, 3) - 4*f(x).diff(x, 2) + \
        4*f(x).diff(x),
        'sol': [Eq(f(x), C1 + C2*exp(-2*x) + C3*exp(x) + C4*exp(2*x))],
        'slow': True,
    },

    'reducible_07': {
        'eq': f(x).diff(x, 4) + 3*f(x).diff(x, 3),
        'sol': [Eq(f(x), C1 + C2*x + C3*x**2 + C4*exp(-3*x))],
        'slow': True,
    },

    'reducible_08': {
        'eq': f(x).diff(x, 4) - 2*f(x).diff(x, 2),
        'sol': [Eq(f(x), C1 + C2*x + C3*exp(-sqrt(2)*x) + C4*exp(sqrt(2)*x))],
        'slow': True,
    },

    'reducible_09': {
        'eq': f(x).diff(x, 4) + 4*f(x).diff(x, 2),
        'sol': [Eq(f(x), C1 + C2*x + C3*sin(2*x) + C4*cos(2*x))],
        'slow': True,
    },

    'reducible_10': {
        'eq': f(x).diff(x, 5) + 2*f(x).diff(x, 3) + f(x).diff(x),
        'sol': [Eq(f(x), C1 + C2*x*sin(x) + C2*cos(x) - C3*x*cos(x) + C3*sin(x) + C4*sin(x) + C5*cos(x))],
        'slow': True,
    },

    'reducible_11': {
        'eq': f(x).diff(x, 2) - f(x).diff(x)**3,
        'sol': [Eq(f(x), C1 - sqrt(2)*sqrt(-1/(C2 + x))*(C2 + x)),
        Eq(f(x), C1 + sqrt(2)*sqrt(-1/(C2 + x))*(C2 + x))],
        'slow': True,
    },

    # Needs to be a way to know how to combine derivatives in the expression
    'reducible_12': {
        'eq': Derivative(x*f(x), x, x, x) + Derivative(f(x), x, x, x),
        'sol': [Eq(f(x), C1 + C3/Mul(2, (x**2 + 2*x + 1), evaluate=False) +
        x*(C2 + C3/Mul(2, (x**2 + 2*x + 1), evaluate=False)))], # 2-arg Mul!
        'slow': True,
    },
    }
    }

