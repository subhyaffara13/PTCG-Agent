
def _get_examples_ode_sol_1st_exact():
    # Type: Exact differential equation, p(x,f) + q(x,f)*f' == 0,
    # where dp/df == dq/dx
    '''
    Example 7 is an exact equation that fails under the exact engine. It is caught
    by first order homogeneous albeit with a much contorted solution.  The
    exact engine fails because of a poorly simplified integral of q(0,y)dy,
    where q is the function multiplying f'.  The solutions should be
    Eq(sqrt(x**2+f(x)**2)**3+y**3, C1).  The equation below is
    equivalent, but it is so complex that checkodesol fails, and takes a long
    time to do so.
    '''
    return {
            'hint': "1st_exact",
            'func': f(x),
            'examples':{
    '1st_exact_01': {
        'eq': sin(x)*cos(f(x)) + cos(x)*sin(f(x))*f(x).diff(x),
        'sol': [Eq(f(x), -acos(C1/cos(x)) + 2*pi), Eq(f(x), acos(C1/cos(x)))],
        'slow': True,
    },

    '1st_exact_02': {
        'eq': (2*x*f(x) + 1)/f(x) + (f(x) - x)/f(x)**2*f(x).diff(x),
        'sol': [Eq(f(x), exp(C1 - x**2 + LambertW(-x*exp(-C1 + x**2))))],
        'XFAIL': ['lie_group'], #It shows dsolve raises an exception: List index out of range for lie_group
        'slow': True,
        'checkodesol_XFAIL':True
    },

    '1st_exact_03': {
        'eq': 2*x + f(x)*cos(x) + (2*f(x) + sin(x) - sin(f(x)))*f(x).diff(x),
        'sol': [Eq(f(x)*sin(x) + cos(f(x)) + x**2 + f(x)**2, C1)],
        'XFAIL': ['lie_group'], #It goes into infinite loop for lie_group.
        'slow': True,
    },

    '1st_exact_04': {
        'eq': cos(f(x)) - (x*sin(f(x)) - f(x)**2)*f(x).diff(x),
        'sol': [Eq(x*cos(f(x)) + f(x)**3/3, C1)],
        'slow': True,
    },

    '1st_exact_05': {
        'eq': 2*x*f(x) + (x**2 + f(x)**2)*f(x).diff(x),
        'sol': [Eq(x**2*f(x) + f(x)**3/3, C1)],
        'slow': True,
        'simplify_flag':False
    },

    # This was from issue: https://github.com/sympy/sympy/issues/11290
    '1st_exact_06': {
        'eq': cos(f(x)) - (x*sin(f(x)) - f(x)**2)*f(x).diff(x),
        'sol': [Eq(x*cos(f(x)) + f(x)**3/3, C1)],
        'simplify_flag':False
    },

    '1st_exact_07': {
        'eq': x*sqrt(x**2 + f(x)**2) - (x**2*f(x)/(f(x) - sqrt(x**2 + f(x)**2)))*f(x).diff(x),
        'sol': [Eq(log(x),
        C1 - 9*sqrt(1 + f(x)**2/x**2)*asinh(f(x)/x)/(-27*f(x)/x +
        27*sqrt(1 + f(x)**2/x**2)) - 9*sqrt(1 + f(x)**2/x**2)*
        log(1 - sqrt(1 + f(x)**2/x**2)*f(x)/x + 2*f(x)**2/x**2)/
        (-27*f(x)/x + 27*sqrt(1 + f(x)**2/x**2)) +
        9*asinh(f(x)/x)*f(x)/(x*(-27*f(x)/x + 27*sqrt(1 + f(x)**2/x**2))) +
        9*f(x)*log(1 - sqrt(1 + f(x)**2/x**2)*f(x)/x + 2*f(x)**2/x**2)/
        (x*(-27*f(x)/x + 27*sqrt(1 + f(x)**2/x**2))))],
        'slow': True,
        'dsolve_too_slow':True
    },

    # Type: a(x)f'(x)+b(x)*f(x)+c(x)=0
    '1st_exact_08': {
        'eq': Eq(x**2*f(x).diff(x) + 3*x*f(x) - sin(x)/x, 0),
        'sol': [Eq(f(x), (C1 - cos(x))/x**3)],
    },

    # these examples are from test_exact_enhancement
    '1st_exact_09': {
        'eq': f(x)/x**2 + ((f(x)*x - 1)/x)*f(x).diff(x),
        'sol': [Eq(f(x), (i*sqrt(C1*x**2 + 1) + 1)/x) for i in (-1, 1)],
    },

    '1st_exact_10': {
        'eq': (x*f(x) - 1) + f(x).diff(x)*(x**2 - x*f(x)),
        'sol': [Eq(f(x), x - sqrt(C1 + x**2 - 2*log(x))), Eq(f(x), x + sqrt(C1 + x**2 - 2*log(x)))],
    },

    '1st_exact_11': {
        'eq': (x + 2)*sin(f(x)) + f(x).diff(x)*x*cos(f(x)),
        'sol': [Eq(f(x), -asin(C1*exp(-x)/x**2) + pi), Eq(f(x), asin(C1*exp(-x)/x**2))],
    },
    }
    }

