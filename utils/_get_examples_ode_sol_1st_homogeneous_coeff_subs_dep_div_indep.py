
def _get_examples_ode_sol_1st_homogeneous_coeff_subs_dep_div_indep():
    return {
            'hint': "1st_homogeneous_coeff_subs_dep_div_indep",
            'func': f(x),
            'examples':{
    'dep_div_indep_01': {
        'eq': f(x)/x*cos(f(x)/x) - (x/f(x)*sin(f(x)/x) + cos(f(x)/x))*f(x).diff(x),
        'sol': [Eq(log(x), C1 - log(f(x)*sin(f(x)/x)/x))],
        'slow': True
    },

    #indep_div_dep actually has a simpler solution for example 2 but it runs too slow.
    'dep_div_indep_02': {
        'eq': x*f(x).diff(x) - f(x) - x*sin(f(x)/x),
        'sol': [Eq(log(x), log(C1) + log(cos(f(x)/x) - 1)/2 - log(cos(f(x)/x) + 1)/2)],
        'simplify_flag':False,
    },

    'dep_div_indep_03': {
        'eq': x*exp(f(x)/x) - f(x)*sin(f(x)/x) + x*sin(f(x)/x)*f(x).diff(x),
        'sol': [Eq(log(x), C1 + exp(-f(x)/x)*sin(f(x)/x)/2 + exp(-f(x)/x)*cos(f(x)/x)/2)],
        'slow': True
    },

    'dep_div_indep_04': {
        'eq': f(x).diff(x) - f(x)/x + 1/sin(f(x)/x),
        'sol': [Eq(f(x), x*(-acos(C1 + log(x)) + 2*pi)), Eq(f(x), x*acos(C1 + log(x)))],
        'slow': True
    },

    # previous code was testing with these other solution:
    # example5_solb = Eq(f(x), log(log(C1/x)**(-x)))
    'dep_div_indep_05': {
        'eq': x*exp(f(x)/x) + f(x) - x*f(x).diff(x),
        'sol': [Eq(f(x), log((1/(C1 - log(x)))**x))],
        'checkodesol_XFAIL':True, #(because of **x?)
    },
    }
    }

