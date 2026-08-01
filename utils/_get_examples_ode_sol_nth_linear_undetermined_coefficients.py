
def _get_examples_ode_sol_nth_linear_undetermined_coefficients():
    # examples 3-27 below are from Ordinary Differential Equations,
    #                     Tenenbaum and Pollard, pg. 231
    g = exp(-x)
    f2 = f(x).diff(x, 2)
    c = 3*f(x).diff(x, 3) + 5*f2 + f(x).diff(x) - f(x) - x
    t = symbols("t")
    u = symbols("u",cls=Function)
    R, L, C, E_0, alpha = symbols("R L C E_0 alpha",positive=True)
    omega = Symbol('omega')
    return {
            'hint': "nth_linear_constant_coeff_undetermined_coefficients",
            'func': f(x),
            'examples':{
    'undet_01': {
        'eq': c - x*g,
        'sol': [Eq(f(x), C3*exp(x/3) - x + (C1 + x*(C2 - x**2/24 - 3*x/32))*exp(-x) - 1)],
        'slow': True,
    },

    'undet_02': {
        'eq': c - g,
        'sol': [Eq(f(x), C3*exp(x/3) - x + (C1 + x*(C2 - x/8))*exp(-x) - 1)],
        'slow': True,
    },

    'undet_03': {
        'eq': f2 + 3*f(x).diff(x) + 2*f(x) - 4,
        'sol': [Eq(f(x), C1*exp(-2*x) + C2*exp(-x) + 2)],
        'slow': True,
    },

    'undet_04': {
        'eq': f2 + 3*f(x).diff(x) + 2*f(x) - 12*exp(x),
        'sol': [Eq(f(x), C1*exp(-2*x) + C2*exp(-x) + 2*exp(x))],
        'slow': True,
    },

    'undet_05': {
        'eq': f2 + 3*f(x).diff(x) + 2*f(x) - exp(I*x),
        'sol': [Eq(f(x), (S(3)/10 + I/10)*(C1*exp(-2*x) + C2*exp(-x) - I*exp(I*x)))],
        'slow': True,
    },

    'undet_06': {
        'eq': f2 + 3*f(x).diff(x) + 2*f(x) - sin(x),
        'sol': [Eq(f(x), C1*exp(-2*x) + C2*exp(-x) + sin(x)/10 - 3*cos(x)/10)],
        'slow': True,
    },

    'undet_07': {
        'eq': f2 + 3*f(x).diff(x) + 2*f(x) - cos(x),
        'sol': [Eq(f(x), C1*exp(-2*x) + C2*exp(-x) + 3*sin(x)/10 + cos(x)/10)],
        'slow': True,
    },

    'undet_08': {
        'eq': f2 + 3*f(x).diff(x) + 2*f(x) - (8 + 6*exp(x) + 2*sin(x)),
        'sol': [Eq(f(x), C1*exp(-2*x) + C2*exp(-x) + exp(x) + sin(x)/5 - 3*cos(x)/5 + 4)],
        'slow': True,
    },

    'undet_09': {
        'eq': f2 + f(x).diff(x) + f(x) - x**2,
        'sol': [Eq(f(x), -2*x + x**2 + (C1*sin(x*sqrt(3)/2) + C2*cos(x*sqrt(3)/2))*exp(-x/2))],
        'slow': True,
    },

    'undet_10': {
        'eq': f2 - 2*f(x).diff(x) - 8*f(x) - 9*x*exp(x) - 10*exp(-x),
        'sol': [Eq(f(x), -x*exp(x) - 2*exp(-x) + C1*exp(-2*x) + C2*exp(4*x))],
        'slow': True,
    },

    'undet_11': {
        'eq': f2 - 3*f(x).diff(x) - 2*exp(2*x)*sin(x),
        'sol': [Eq(f(x), C1 + C2*exp(3*x) - 3*exp(2*x)*sin(x)/5 - exp(2*x)*cos(x)/5)],
        'slow': True,
    },

    'undet_12': {
        'eq': f(x).diff(x, 4) - 2*f2 + f(x) - x + sin(x),
        'sol': [Eq(f(x), x - sin(x)/4 + (C1 + C2*x)*exp(-x) + (C3 + C4*x)*exp(x))],
        'slow': True,
    },

    'undet_13': {
        'eq': f2 + f(x).diff(x) - x**2 - 2*x,
        'sol': [Eq(f(x), C1 + x**3/3 + C2*exp(-x))],
        'slow': True,
    },

    'undet_14': {
        'eq': f2 + f(x).diff(x) - x - sin(2*x),
        'sol': [Eq(f(x), C1 - x - sin(2*x)/5 - cos(2*x)/10 + x**2/2 + C2*exp(-x))],
        'slow': True,
    },

    'undet_15': {
        'eq': f2 + f(x) - 4*x*sin(x),
        'sol': [Eq(f(x), (C1 - x**2)*cos(x) + (C2 + x)*sin(x))],
        'slow': True,
    },

    'undet_16': {
        'eq': f2 + 4*f(x) - x*sin(2*x),
        'sol': [Eq(f(x), (C1 - x**2/8)*cos(2*x) + (C2 + x/16)*sin(2*x))],
        'slow': True,
    },

    'undet_17': {
        'eq': f2 + 2*f(x).diff(x) + f(x) - x**2*exp(-x),
        'sol': [Eq(f(x), (C1 + x*(C2 + x**3/12))*exp(-x))],
        'slow': True,
    },

    'undet_18': {
        'eq': f(x).diff(x, 3) + 3*f2 + 3*f(x).diff(x) + f(x) - 2*exp(-x) + \
        x**2*exp(-x),
        'sol': [Eq(f(x), (C1 + x*(C2 + x*(C3 - x**3/60 + x/3)))*exp(-x))],
        'slow': True,
    },

    'undet_19': {
        'eq': f2 + 3*f(x).diff(x) + 2*f(x) - exp(-2*x) - x**2,
        'sol': [Eq(f(x), C2*exp(-x) + x**2/2 - x*Rational(3,2) + (C1 - x)*exp(-2*x) + Rational(7,4))],
        'slow': True,
    },

    'undet_20': {
        'eq': f2 - 3*f(x).diff(x) + 2*f(x) - x*exp(-x),
        'sol': [Eq(f(x), C1*exp(x) + C2*exp(2*x) + (6*x + 5)*exp(-x)/36)],
        'slow': True,
    },

    'undet_21': {
        'eq': f2 + f(x).diff(x) - 6*f(x) - x - exp(2*x),
        'sol': [Eq(f(x), Rational(-1, 36) - x/6 + C2*exp(-3*x) + (C1 + x/5)*exp(2*x))],
        'slow': True,
    },

    'undet_22': {
        'eq': f2 + f(x) - sin(x) - exp(-x),
        'sol': [Eq(f(x), C2*sin(x) + (C1 - x/2)*cos(x) + exp(-x)/2)],
        'slow': True,
    },

    'undet_23': {
        'eq': f(x).diff(x, 3) - 3*f2 + 3*f(x).diff(x) - f(x) - exp(x),
        'sol': [Eq(f(x), (C1 + x*(C2 + x*(C3 + x/6)))*exp(x))],
        'slow': True,
    },

    'undet_24': {
        'eq': f2 + f(x) - S.Half - cos(2*x)/2,
        'sol': [Eq(f(x), S.Half - cos(2*x)/6 + C1*sin(x) + C2*cos(x))],
        'slow': True,
    },

    'undet_25': {
        'eq': f(x).diff(x, 3) - f(x).diff(x) - exp(2*x)*(S.Half - cos(2*x)/2),
        'sol': [Eq(f(x), C1 + C2*exp(-x) + C3*exp(x) + (-21*sin(2*x) + 27*cos(2*x) + 130)*exp(2*x)/1560)],
        'slow': True,
    },

    #Note: 'undet_26' is referred in 'undet_37'
    'undet_26': {
        'eq': (f(x).diff(x, 5) + 2*f(x).diff(x, 3) + f(x).diff(x) - 2*x -
        sin(x) - cos(x)),
        'sol': [Eq(f(x), C1 + x**2 + (C2 + x*(C3 - x/8))*sin(x) + (C4 + x*(C5 + x/8))*cos(x))],
        'slow': True,
    },

    'undet_27': {
        'eq': f2 + f(x) - cos(x)/2 + cos(3*x)/2,
        'sol': [Eq(f(x), cos(3*x)/16 + C2*cos(x) + (C1 + x/4)*sin(x))],
        'slow': True,
    },

    'undet_28': {
        'eq': f(x).diff(x) - 1,
        'sol': [Eq(f(x), C1 + x)],
        'slow': True,
    },

    # https://github.com/sympy/sympy/issues/19358
    'undet_29': {
        'eq': f2 + f(x).diff(x) + exp(x-C1),
        'sol': [Eq(f(x), C2 + C3*exp(-x) - exp(-C1 + x)/2)],
        'slow': True,
    },

    # https://github.com/sympy/sympy/issues/18408
    'undet_30': {
        'eq': f(x).diff(x, 3) - f(x).diff(x) - sinh(x),
        'sol': [Eq(f(x), C1 + C2*exp(-x) + C3*exp(x) + x*sinh(x)/2)],
    },

    'undet_31': {
        'eq': f(x).diff(x, 2) - 49*f(x) - sinh(3*x),
        'sol': [Eq(f(x), C1*exp(-7*x) + C2*exp(7*x) - sinh(3*x)/40)],
    },

    'undet_32': {
        'eq': f(x).diff(x, 3) - f(x).diff(x) - sinh(x) - exp(x),
        'sol': [Eq(f(x), C1 + C3*exp(-x) + x*sinh(x)/2 + (C2 + x/2)*exp(x))],
    },

    # https://github.com/sympy/sympy/issues/5096
    'undet_33': {
        'eq': f(x).diff(x, x) + f(x) - x*sin(x - 2),
        'sol': [Eq(f(x), C1*sin(x) + C2*cos(x) - x**2*cos(x - 2)/4 + x*sin(x - 2)/4)],
    },

    'undet_34': {
        'eq': f(x).diff(x, 2) + f(x) - x**4*sin(x-1),
        'sol': [ Eq(f(x), C1*sin(x) + C2*cos(x) - x**5*cos(x - 1)/10 + x**4*sin(x - 1)/4 + x**3*cos(x - 1)/2 - 3*x**2*sin(x - 1)/4 - 3*x*cos(x - 1)/4)],
    },

    'undet_35': {
        'eq': f(x).diff(x, 2) - f(x) - exp(x - 1),
        'sol': [Eq(f(x), C2*exp(-x) + (C1 + x*exp(-1)/2)*exp(x))],
    },

    'undet_36': {
        'eq': f(x).diff(x, 2)+f(x)-(sin(x-2)+1),
        'sol': [Eq(f(x), C1*sin(x) + C2*cos(x) - x*cos(x - 2)/2 + 1)],
    },

    # Equivalent to example_name 'undet_26'.
    # This previously failed because the algorithm for undetermined coefficients
    # didn't know to multiply exp(I*x) by sufficient x because it is linearly
    # dependent on sin(x) and cos(x).
    'undet_37': {
        'eq': f(x).diff(x, 5) + 2*f(x).diff(x, 3) + f(x).diff(x) - 2*x - exp(I*x),
        'sol': [Eq(f(x), C1 + x**2*(I*exp(I*x)/8 + 1) + (C2 + C3*x)*sin(x) + (C4 + C5*x)*cos(x))],
    },

    # https://github.com/sympy/sympy/issues/12623
    'undet_38': {
        'eq': Eq( u(t).diff(t,t) + R /L*u(t).diff(t) + 1/(L*C)*u(t), alpha),
        'sol': [Eq(u(t), C*L*alpha + C2*exp(-t*(R + sqrt(C*R**2 - 4*L)/sqrt(C))/(2*L))
        + C1*exp(t*(-R + sqrt(C*R**2 - 4*L)/sqrt(C))/(2*L)))],
        'func': u(t)
    },

    'undet_39': {
        'eq': Eq( L*C*u(t).diff(t,t) + R*C*u(t).diff(t) + u(t), E_0*exp(I*omega*t) ),
        'sol': [Eq(u(t), C2*exp(-t*(R + sqrt(C*R**2 - 4*L)/sqrt(C))/(2*L))
        + C1*exp(t*(-R + sqrt(C*R**2 - 4*L)/sqrt(C))/(2*L))
        - E_0*exp(I*omega*t)/(C*L*omega**2 - I*C*R*omega - 1))],
        'func': u(t),
    },

    # https://github.com/sympy/sympy/issues/6879
    'undet_40': {
        'eq': Eq(Derivative(f(x), x, 2) - 2*Derivative(f(x), x) + f(x), sin(x)),
        'sol': [Eq(f(x), (C1 + C2*x)*exp(x) + cos(x)/2)],
    },
    }
    }

