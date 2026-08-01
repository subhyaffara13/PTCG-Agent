
def _get_examples_ode_sol_1st_homogeneous_coeff_best():
    return {
            'hint': "1st_homogeneous_coeff_best",
            'func': f(x),
            'examples':{
    # previous code was testing this with other solution:
    # example1_solb = Eq(-f(x)/(1 + log(x/f(x))), C1)
    '1st_homogeneous_coeff_best_01': {
        'eq': f(x) + (x*log(f(x)/x) - 2*x)*diff(f(x), x),
        'sol': [Eq(f(x), -exp(C1)*LambertW(-x*exp(-C1 + 1)))],
        'checkodesol_XFAIL':True, #(because of LambertW?)
    },

    '1st_homogeneous_coeff_best_02': {
        'eq': 2*f(x)*exp(x/f(x)) + f(x)*f(x).diff(x) - 2*x*exp(x/f(x))*f(x).diff(x),
        'sol': [Eq(log(f(x)), C1 - 2*exp(x/f(x)))],
    },

    # previous code was testing this with other solution:
    # example3_solb = Eq(log(C1*x*sqrt(1/x)*sqrt(f(x))) + x**2/(2*f(x)**2), 0)
    '1st_homogeneous_coeff_best_03': {
        'eq': 2*x**2*f(x) + f(x)**3 + (x*f(x)**2 - 2*x**3)*f(x).diff(x),
        'sol': [Eq(f(x), exp(2*C1 + LambertW(-2*x**4*exp(-4*C1))/2)/x)],
        'checkodesol_XFAIL':True,  #(because of LambertW?)
    },

    '1st_homogeneous_coeff_best_04': {
        'eq': (x + sqrt(f(x)**2 - x*f(x)))*f(x).diff(x) - f(x),
        'sol': [Eq(log(f(x)), C1 - 2*sqrt(-x/f(x) + 1))],
        'slow': True,
    },

    '1st_homogeneous_coeff_best_05': {
        'eq': x + f(x) - (x - f(x))*f(x).diff(x),
        'sol': [Eq(log(x), C1 - log(sqrt(1 + f(x)**2/x**2)) + atan(f(x)/x))],
    },

    '1st_homogeneous_coeff_best_06': {
        'eq': x*f(x).diff(x) - f(x) - x*sin(f(x)/x),
        'sol': [Eq(f(x), 2*x*atan(C1*x))],
    },

    '1st_homogeneous_coeff_best_07': {
        'eq': x**2 + f(x)**2 - 2*x*f(x)*f(x).diff(x),
        'sol': [Eq(f(x), -sqrt(x*(C1 + x))), Eq(f(x), sqrt(x*(C1 + x)))],
    },

    '1st_homogeneous_coeff_best_08': {
        'eq': f(x)**2 + (x*sqrt(f(x)**2 - x**2) - x*f(x))*f(x).diff(x),
        'sol': [Eq(f(x), -C1*sqrt(-x/(x - 2*C1))), Eq(f(x), C1*sqrt(-x/(x - 2*C1)))],
        'checkodesol_XFAIL': True  # solutions are valid in a range
    },
    }
    }

