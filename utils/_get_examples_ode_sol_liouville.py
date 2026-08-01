
def _get_examples_ode_sol_liouville():
    n = Symbol('n')
    _y = Dummy('y')
    return {
            'hint': "Liouville",
            'func': f(x),
            'examples':{
    'liouville_01': {
        'eq': diff(f(x), x)/x + diff(f(x), x, x)/2 - diff(f(x), x)**2/2,
        'sol': [Eq(f(x), log(x/(C1 + C2*x)))],

    },

    'liouville_02': {
        'eq': diff(x*exp(-f(x)), x, x),
        'sol': [Eq(f(x), log(x/(C1 + C2*x)))]
    },

    'liouville_03': {
        'eq':  ((diff(f(x), x)/x + diff(f(x), x, x)/2 - diff(f(x), x)**2/2)*exp(-f(x))/exp(f(x))).expand(),
        'sol': [Eq(f(x), log(x/(C1 + C2*x)))]
    },

    'liouville_04': {
        'eq': diff(f(x), x, x) + 1/f(x)*(diff(f(x), x))**2 + 1/x*diff(f(x), x),
        'sol': [Eq(f(x), -sqrt(C1 + C2*log(x))), Eq(f(x), sqrt(C1 + C2*log(x)))],
    },

    'liouville_05': {
        'eq': x*diff(f(x), x, x) + x/f(x)*diff(f(x), x)**2 + x*diff(f(x), x),
        'sol': [Eq(f(x), -sqrt(C1 + C2*exp(-x))), Eq(f(x), sqrt(C1 + C2*exp(-x)))],
    },

    'liouville_06': {
        'eq': Eq((x*exp(f(x))).diff(x, x), 0),
        'sol': [Eq(f(x), log(C1 + C2/x))],
    },

    'liouville_07': {
        'eq': (diff(f(x), x)/x + diff(f(x), x, x)/2 - diff(f(x), x)**2/2)*exp(-f(x))/exp(f(x)),
        'sol': [Eq(f(x), log(x/(C1 + C2*x)))],
    },

    'liouville_08': {
        'eq': x**2*diff(f(x),x) + (n*f(x) + f(x)**2)*diff(f(x),x)**2 + diff(f(x), (x, 2)),
        'sol': [Eq(C1 + C2*lowergamma(Rational(1,3), x**3/3) + NonElementaryIntegral(exp(_y**3/3)*exp(_y**2*n/2), (_y, f(x))), 0)],
    },
    }
    }

