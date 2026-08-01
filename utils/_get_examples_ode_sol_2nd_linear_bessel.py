
def _get_examples_ode_sol_2nd_linear_bessel():
    return {
            'hint': "2nd_linear_bessel",
            'func': f(x),
            'examples':{
    '2nd_lin_bessel_01': {
        'eq': x**2*(f(x).diff(x, 2)) + x*(f(x).diff(x)) + (x**2 - 4)*f(x),
        'sol': [Eq(f(x), C1*besselj(2, x) + C2*bessely(2, x))],
    },

    '2nd_lin_bessel_02': {
        'eq': x**2*(f(x).diff(x, 2)) + x*(f(x).diff(x)) + (x**2 +25)*f(x),
        'sol': [Eq(f(x), C1*besselj(5*I, x) + C2*bessely(5*I, x))],
    },

    '2nd_lin_bessel_03': {
        'eq': x**2*(f(x).diff(x, 2)) + x*(f(x).diff(x)) + (x**2)*f(x),
        'sol': [Eq(f(x), C1*besselj(0, x) + C2*bessely(0, x))],
    },

    '2nd_lin_bessel_04': {
        'eq': x**2*(f(x).diff(x, 2)) + x*(f(x).diff(x)) + (81*x**2 -S(1)/9)*f(x),
        'sol': [Eq(f(x), C1*besselj(S(1)/3, 9*x) + C2*bessely(S(1)/3, 9*x))],
    },

    '2nd_lin_bessel_05': {
        'eq': x**2*(f(x).diff(x, 2)) + x*(f(x).diff(x)) + (x**4 - 4)*f(x),
        'sol': [Eq(f(x), C1*besselj(1, x**2/2) + C2*bessely(1, x**2/2))],
    },

    '2nd_lin_bessel_06': {
        'eq': x**2*(f(x).diff(x, 2)) + 2*x*(f(x).diff(x)) + (x**4 - 4)*f(x),
        'sol': [Eq(f(x), (C1*besselj(sqrt(17)/4, x**2/2) + C2*bessely(sqrt(17)/4, x**2/2))/sqrt(x))],
    },

    '2nd_lin_bessel_07': {
        'eq': x**2*(f(x).diff(x, 2)) + x*(f(x).diff(x)) + (x**2 - S(1)/4)*f(x),
        'sol': [Eq(f(x), C1*besselj(S(1)/2, x) + C2*bessely(S(1)/2, x))],
    },

    '2nd_lin_bessel_08': {
        'eq': x**2*(f(x).diff(x, 2)) - 3*x*(f(x).diff(x)) + (4*x + 4)*f(x),
        'sol': [Eq(f(x), x**2*(C1*besselj(0, 4*sqrt(x)) + C2*bessely(0, 4*sqrt(x))))],
    },

    '2nd_lin_bessel_09': {
        'eq': x*(f(x).diff(x, 2)) - f(x).diff(x) + 4*x**3*f(x),
        'sol': [Eq(f(x), x*(C1*besselj(S(1)/2, x**2) + C2*bessely(S(1)/2, x**2)))],
    },

    '2nd_lin_bessel_10': {
        'eq': (x-2)**2*(f(x).diff(x, 2)) - (x-2)*f(x).diff(x) + 4*(x-2)**2*f(x),
        'sol': [Eq(f(x), (x - 2)*(C1*besselj(1, 2*x - 4) + C2*bessely(1, 2*x - 4)))],
    },

    # https://github.com/sympy/sympy/issues/4414
    '2nd_lin_bessel_11': {
        'eq': f(x).diff(x, x) + 2/x*f(x).diff(x) + f(x),
        'sol': [Eq(f(x), (C1*besselj(S(1)/2, x) + C2*bessely(S(1)/2, x))/sqrt(x))],
    },
    '2nd_lin_bessel_12': {
        'eq': x**2*f(x).diff(x, 2) + x*f(x).diff(x) + (a**2*x**2/c**2 - b**2)*f(x),
        'sol': [Eq(f(x), C1*besselj(sqrt(b**2), x*sqrt(a**2/c**2)) + C2*bessely(sqrt(b**2), x*sqrt(a**2/c**2)))],
    },
    }
    }

