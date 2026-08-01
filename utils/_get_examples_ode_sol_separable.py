
def _get_examples_ode_sol_separable():
    # test_separable1-5 are from Ordinary Differential Equations, Tenenbaum and
    # Pollard, pg. 55
    t,a = symbols('a,t')
    m = 96
    g = 9.8
    k = .2
    f1 = g * m
    v = Function('v')
    return {
            'hint': "separable",
            'func': f(x),
            'examples':{
    'separable_01': {
        'eq': f(x).diff(x) - f(x),
        'sol': [Eq(f(x), C1*exp(x))],
    },

    'separable_02': {
        'eq': x*f(x).diff(x) - f(x),
        'sol': [Eq(f(x), C1*x)],
    },

    'separable_03': {
        'eq': f(x).diff(x) + sin(x),
        'sol': [Eq(f(x), C1 + cos(x))],
    },

    'separable_04': {
        'eq': f(x)**2 + 1 - (x**2 + 1)*f(x).diff(x),
        'sol': [Eq(f(x), tan(C1 + atan(x)))],
    },

    'separable_05': {
        'eq': f(x).diff(x)/tan(x) - f(x) - 2,
        'sol': [Eq(f(x), C1/cos(x) - 2)],
    },

    'separable_06': {
        'eq': f(x).diff(x) * (1 - sin(f(x))) - 1,
        'sol': [Eq(-x + f(x) + cos(f(x)), C1)],
    },

    'separable_07': {
        'eq': f(x)*x**2*f(x).diff(x) - f(x)**3 - 2*x**2*f(x).diff(x),
        'sol': [Eq(f(x), (-x - sqrt(x*(4*C1*x + x - 4)))/(C1*x - 1)/2),
                Eq(f(x), (-x + sqrt(x*(4*C1*x + x - 4)))/(C1*x - 1)/2)],
        'slow': True,
    },

    'separable_08': {
        'eq': f(x)**2 - 1 - (2*f(x) + x*f(x))*f(x).diff(x),
        'sol': [Eq(f(x), -sqrt(C1*x**2 + 4*C1*x + 4*C1 + 1)),
        Eq(f(x), sqrt(C1*x**2 + 4*C1*x + 4*C1 + 1))],
        'slow': True,
    },

    'separable_09': {
        'eq': x*log(x)*f(x).diff(x) + sqrt(1 + f(x)**2),
        'sol': [Eq(f(x), sinh(C1 - log(log(x))))],  #One more solution is f(x)=I
        'slow': True,
        'checkodesol_XFAIL': True,
    },

    'separable_10': {
        'eq': exp(x + 1)*tan(f(x)) + cos(f(x))*f(x).diff(x),
        'sol': [Eq(E*exp(x) + log(cos(f(x)) - 1)/2 - log(cos(f(x)) + 1)/2 + cos(f(x)), C1)],
        'slow': True,
    },

    'separable_11': {
        'eq': (x*cos(f(x)) + x**2*sin(f(x))*f(x).diff(x) - a**2*sin(f(x))*f(x).diff(x)),
        'sol': [
            Eq(f(x), -acos(C1*sqrt(-a**2 + x**2)) + 2*pi),
            Eq(f(x), acos(C1*sqrt(-a**2 + x**2)))
        ],
        'slow': True,
    },

    'separable_12': {
        'eq': f(x).diff(x) - f(x)*tan(x),
        'sol': [Eq(f(x), C1/cos(x))],
    },

    'separable_13': {
        'eq': (x - 1)*cos(f(x))*f(x).diff(x) - 2*x*sin(f(x)),
        'sol': [
            Eq(f(x), pi - asin(C1*(x**2 - 2*x + 1)*exp(2*x))),
            Eq(f(x), asin(C1*(x**2 - 2*x + 1)*exp(2*x)))
        ],
    },

    'separable_14': {
        'eq': f(x).diff(x) - f(x)*log(f(x))/tan(x),
        'sol': [Eq(f(x), exp(C1*sin(x)))],
    },

    'separable_15': {
        'eq': x*f(x).diff(x) + (1 + f(x)**2)*atan(f(x)),
        'sol': [Eq(f(x), tan(C1/x))],  #Two more solutions are f(x)=0 and f(x)=I
        'slow': True,
        'checkodesol_XFAIL': True,
    },

    'separable_16': {
        'eq': f(x).diff(x) + x*(f(x) + 1),
        'sol': [Eq(f(x), -1 + C1*exp(-x**2/2))],
    },

    'separable_17': {
        'eq': exp(f(x)**2)*(x**2 + 2*x + 1) + (x*f(x) + f(x))*f(x).diff(x),
        'sol': [
            Eq(f(x), -sqrt(log(1/(C1 + x**2 + 2*x)))),
            Eq(f(x), sqrt(log(1/(C1 + x**2 + 2*x))))
        ],
    },

    'separable_18': {
        'eq': f(x).diff(x) + f(x),
        'sol': [Eq(f(x), C1*exp(-x))],
    },

    'separable_19': {
        'eq': sin(x)*cos(2*f(x)) + cos(x)*sin(2*f(x))*f(x).diff(x),
        'sol': [Eq(f(x), pi - acos(C1/cos(x)**2)/2), Eq(f(x), acos(C1/cos(x)**2)/2)],
    },

    'separable_20': {
        'eq': (1 - x)*f(x).diff(x) - x*(f(x) + 1),
        'sol': [Eq(f(x), (C1*exp(-x) - x + 1)/(x - 1))],
    },

    'separable_21': {
        'eq': f(x)*diff(f(x), x) + x - 3*x*f(x)**2,
        'sol': [Eq(f(x), -sqrt(3)*sqrt(C1*exp(3*x**2) + 1)/3),
        Eq(f(x), sqrt(3)*sqrt(C1*exp(3*x**2) + 1)/3)],
    },

    'separable_22': {
        'eq': f(x).diff(x) - exp(x + f(x)),
        'sol': [Eq(f(x), log(-1/(C1 + exp(x))))],
        'XFAIL': ['lie_group'] #It shows 'NoneType' object is not subscriptable for lie_group.
    },

    # https://github.com/sympy/sympy/issues/7081
    'separable_23': {
        'eq': x*(f(x).diff(x)) + 1 - f(x)**2,
        'sol': [Eq(f(x), (-C1 - x**2)/(-C1 + x**2))],
    },

    # https://github.com/sympy/sympy/issues/10379
    'separable_24': {
        'eq': f(t).diff(t)-(1-51.05*y*f(t)),
        'sol': [Eq(f(t), (0.019588638589618023*exp(y*(C1 - 51.049999999999997*t)) + 0.019588638589618023)/y)],
        'func': f(t),
    },

    # https://github.com/sympy/sympy/issues/15999
    'separable_25': {
        'eq': f(x).diff(x) - C1*f(x),
        'sol': [Eq(f(x), C2*exp(C1*x))],
    },

    'separable_26': {
        'eq': f1 - k * (v(t) ** 2) - m * Derivative(v(t)),
        'sol': [Eq(v(t), -68.585712797928991/tanh(C1 - 0.14288690166235204*t))],
        'func': v(t),
        'checkodesol_XFAIL': True,
    },

    #https://github.com/sympy/sympy/issues/22155
    'separable_27': {
        'eq': f(x).diff(x) - exp(f(x) - x),
        'sol': [Eq(f(x), log(-exp(x)/(C1*exp(x) - 1)))],
    }
    }
    }

