
def _get_examples_ode_sol_euler_var_para():
    return {
            'hint': "nth_linear_euler_eq_nonhomogeneous_variation_of_parameters",
            'func': f(x),
            'examples':{
    'euler_var_01': {
        'eq': Eq(x**2*Derivative(f(x), x, x) - 2*x*Derivative(f(x), x) + 2*f(x), x**4),
        'sol': [Eq(f(x), x*(C1 + C2*x + x**3/6))]
    },

    'euler_var_02': {
        'eq': Eq(3*x**2*diff(f(x), x, x) + 6*x*diff(f(x), x) - 6*f(x), x**3*exp(x)),
        'sol': [Eq(f(x), C1/x**2 + C2*x + x*exp(x)/3 - 4*exp(x)/3 + 8*exp(x)/(3*x) - 8*exp(x)/(3*x**2))]
    },

    'euler_var_03': {
        'eq': Eq(x**2*Derivative(f(x), x, x) - 2*x*Derivative(f(x), x) + 2*f(x), x**4*exp(x)),
        'sol':  [Eq(f(x), x*(C1 + C2*x + x*exp(x) - 2*exp(x)))]
    },

    'euler_var_04': {
        'eq': x**2*Derivative(f(x), x, x) - 2*x*Derivative(f(x), x) + 2*f(x) - log(x),
        'sol': [Eq(f(x), C1*x + C2*x**2 + log(x)/2 + Rational(3, 4))]
    },

    'euler_var_05': {
        'eq': -exp(x) + (x*Derivative(f(x), (x, 2)) + Derivative(f(x), x))/x,
        'sol': [Eq(f(x), C1 + C2*log(x) + exp(x) - Ei(x))]
    },

    'euler_var_06': {
        'eq': x**2 * f(x).diff(x, 2) + x * f(x).diff(x) + 4 * f(x) - 1/x,
        'sol': [Eq(f(x), C1*sin(2*log(x)) + C2*cos(2*log(x)) + 1/(5*x))]
    },
    }
    }

