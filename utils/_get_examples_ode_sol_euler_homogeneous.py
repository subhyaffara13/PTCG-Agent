
def _get_examples_ode_sol_euler_homogeneous():
    r1, r2, r3, r4, r5 = [rootof(x**5 - 14*x**4 + 71*x**3 - 154*x**2 + 120*x - 1, n) for n in range(5)]
    return {
            'hint': "nth_linear_euler_eq_homogeneous",
            'func': f(x),
            'examples':{
    'euler_hom_01': {
        'eq': Eq(-3*diff(f(x), x)*x + 2*x**2*diff(f(x), x, x), 0),
        'sol': [Eq(f(x), C1 + C2*x**Rational(5, 2))],
    },

    'euler_hom_02': {
        'eq': Eq(3*f(x) - 5*diff(f(x), x)*x + 2*x**2*diff(f(x), x, x), 0),
        'sol': [Eq(f(x), C1*sqrt(x) + C2*x**3)]
    },

    'euler_hom_03': {
        'eq': Eq(4*f(x) + 5*diff(f(x), x)*x + x**2*diff(f(x), x, x), 0),
        'sol': [Eq(f(x), (C1 + C2*log(x))/x**2)]
    },

    'euler_hom_04': {
        'eq': Eq(6*f(x) - 6*diff(f(x), x)*x + 1*x**2*diff(f(x), x, x) + x**3*diff(f(x), x, x, x), 0),
        'sol': [Eq(f(x), C1/x**2 + C2*x + C3*x**3)]
    },

    'euler_hom_05': {
        'eq': Eq(-125*f(x) + 61*diff(f(x), x)*x - 12*x**2*diff(f(x), x, x) + x**3*diff(f(x), x, x, x), 0),
        'sol': [Eq(f(x), x**5*(C1 + C2*log(x) + C3*log(x)**2))]
    },

    'euler_hom_06': {
        'eq': x**2*diff(f(x), x, 2) + x*diff(f(x), x) - 9*f(x),
        'sol': [Eq(f(x), C1*x**-3 + C2*x**3)]
    },

    'euler_hom_07': {
        'eq': sin(x)*x**2*f(x).diff(x, 2) + sin(x)*x*f(x).diff(x) + sin(x)*f(x),
        'sol': [Eq(f(x), C1*sin(log(x)) + C2*cos(log(x)))],
        'XFAIL': ['2nd_power_series_regular','nth_linear_euler_eq_nonhomogeneous_undetermined_coefficients']
    },

    'euler_hom_08': {
        'eq': x**6 * f(x).diff(x, 6) - x*f(x).diff(x) + f(x),
        'sol': [Eq(f(x), C1*x + C2*x**r1 + C3*x**r2 + C4*x**r3 + C5*x**r4 + C6*x**r5)],
        'checkodesol_XFAIL':True
    },

     #This example is from issue: https://github.com/sympy/sympy/issues/15237 #This example is from issue:
     #  https://github.com/sympy/sympy/issues/15237
    'euler_hom_09': {
        'eq': Derivative(x*f(x), x, x, x),
        'sol': [Eq(f(x), C1 + C2/x + C3*x)],
    },
    }
    }

