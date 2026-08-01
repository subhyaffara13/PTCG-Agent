
def _get_examples_ode_sol_lie_group():
    a, b, c = symbols("a b c")
    return {
            'hint': "lie_group",
            'func': f(x),
            'examples':{
    #Example 1-4 and 19-20 were from issue: https://github.com/sympy/sympy/issues/17322
    'lie_group_01': {
        'eq': x*f(x).diff(x)*(f(x)+4) + (f(x)**2) -2*f(x)-2*x,
        'sol': [],
        'dsolve_too_slow': True,
        'checkodesol_too_slow': True,
    },

    'lie_group_02': {
        'eq': x*f(x).diff(x)*(f(x)+4) + (f(x)**2) -2*f(x)-2*x,
        'sol': [],
        'dsolve_too_slow': True,
    },

    'lie_group_03': {
        'eq': Eq(x**7*Derivative(f(x), x) + 5*x**3*f(x)**2 - (2*x**2 + 2)*f(x)**3, 0),
        'sol': [],
        'dsolve_too_slow': True,
    },

    'lie_group_04': {
        'eq': f(x).diff(x) - (f(x) - x*log(x))**2/x**2 + log(x),
        'sol': [],
        'XFAIL': ['lie_group'],
    },

    'lie_group_05': {
        'eq': f(x).diff(x)**2,
        'sol': [Eq(f(x), C1)],
        'XFAIL': ['factorable'],  #It raises Not Implemented error
    },

    'lie_group_06': {
        'eq': Eq(f(x).diff(x), x**2*f(x)),
        'sol': [Eq(f(x), C1*exp(x**3)**Rational(1, 3))],
    },

    'lie_group_07': {
        'eq': f(x).diff(x) + a*f(x) - c*exp(b*x),
        'sol': [Eq(f(x), Piecewise(((-C1*(a + b) + c*exp(x*(a + b)))*exp(-a*x)/(a + b),\
        Ne(a, -b)), ((-C1 + c*x)*exp(-a*x), True)))],
    },

    'lie_group_08': {
        'eq': f(x).diff(x) + 2*x*f(x) - x*exp(-x**2),
        'sol': [Eq(f(x), (C1 + x**2/2)*exp(-x**2))],
    },

    'lie_group_09': {
        'eq': (1 + 2*x)*(f(x).diff(x)) + 2 - 4*exp(-f(x)),
        'sol': [Eq(f(x), log(C1/(2*x + 1) + 2))],
    },

    'lie_group_10': {
        'eq': x**2*(f(x).diff(x)) - f(x) + x**2*exp(x - (1/x)),
        'sol': [Eq(f(x), (C1 - exp(x))*exp(-1/x))],
        'XFAIL': ['factorable'], #It raises Recursion Error (maixmum depth exceeded)
    },

    'lie_group_11': {
        'eq': x**2*f(x)**2 + x*Derivative(f(x), x),
        'sol': [Eq(f(x), 2/(C1 + x**2))],
    },

    'lie_group_12': {
        'eq': diff(f(x),x) + 2*x*f(x) - x*exp(-x**2),
        'sol': [Eq(f(x), exp(-x**2)*(C1 + x**2/2))],
    },

    'lie_group_13': {
        'eq': diff(f(x),x) + f(x)*cos(x) - exp(2*x),
        'sol': [Eq(f(x), exp(-sin(x))*(C1 + Integral(exp(2*x)*exp(sin(x)), x)))],
    },

    'lie_group_14': {
        'eq': diff(f(x),x) + f(x)*cos(x) - sin(2*x)/2,
        'sol': [Eq(f(x), C1*exp(-sin(x)) + sin(x) - 1)],
    },

    'lie_group_15': {
        'eq': x*diff(f(x),x) + f(x) - x*sin(x),
        'sol': [Eq(f(x), (C1 - x*cos(x) + sin(x))/x)],
    },

    'lie_group_16': {
        'eq': x*diff(f(x),x) - f(x) - x/log(x),
        'sol': [Eq(f(x), x*(C1 + log(log(x))))],
    },

    'lie_group_17': {
        'eq': (f(x).diff(x)-f(x)) * (f(x).diff(x)+f(x)),
        'sol': [Eq(f(x), C1*exp(x)), Eq(f(x), C1*exp(-x))],
    },

    'lie_group_18': {
        'eq': f(x).diff(x) * (f(x).diff(x) - f(x)),
        'sol': [Eq(f(x), C1*exp(x)), Eq(f(x), C1)],
    },

    'lie_group_19': {
        'eq': (f(x).diff(x)-f(x)) * (f(x).diff(x)+f(x)),
        'sol': [Eq(f(x), C1*exp(-x)), Eq(f(x), C1*exp(x))],
    },

    'lie_group_20': {
        'eq': f(x).diff(x)*(f(x).diff(x)+f(x)),
        'sol': [Eq(f(x), C1), Eq(f(x), C1*exp(-x))],
    },
    }
    }

