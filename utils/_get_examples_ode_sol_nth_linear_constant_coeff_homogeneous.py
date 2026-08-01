
def _get_examples_ode_sol_nth_linear_constant_coeff_homogeneous():
    # From Exercise 20, in Ordinary Differential Equations,
    #                      Tenenbaum and Pollard, pg. 220
    a = Symbol('a', positive=True)
    k = Symbol('k', real=True)
    r1, r2, r3, r4, r5 = [rootof(x**5 + 11*x - 2, n) for n in range(5)]
    r6, r7, r8, r9, r10 = [rootof(x**5 - 3*x + 1, n) for n in range(5)]
    r11, r12, r13, r14, r15 = [rootof(x**5 - 100*x**3 + 1000*x + 1, n) for n in range(5)]
    r16, r17, r18, r19, r20 = [rootof(x**5 - x**4 + 10, n) for n in range(5)]
    r21, r22, r23, r24, r25 = [rootof(x**5 - x + 1, n) for n in range(5)]
    E = exp(1)
    return {
            'hint': "nth_linear_constant_coeff_homogeneous",
            'func': f(x),
            'examples':{
    'lin_const_coeff_hom_01': {
        'eq': f(x).diff(x, 2) + 2*f(x).diff(x),
        'sol': [Eq(f(x), C1 + C2*exp(-2*x))],
    },

    'lin_const_coeff_hom_02': {
        'eq': f(x).diff(x, 2) - 3*f(x).diff(x) + 2*f(x),
        'sol': [Eq(f(x), (C1 + C2*exp(x))*exp(x))],
    },

    'lin_const_coeff_hom_03': {
        'eq': f(x).diff(x, 2) - f(x),
        'sol': [Eq(f(x), C1*exp(-x) + C2*exp(x))],
    },

    'lin_const_coeff_hom_04': {
        'eq': f(x).diff(x, 3) + f(x).diff(x, 2) - 6*f(x).diff(x),
        'sol': [Eq(f(x), C1 + C2*exp(-3*x) + C3*exp(2*x))],
        'slow': True,
    },

    'lin_const_coeff_hom_05': {
        'eq': 6*f(x).diff(x, 2) - 11*f(x).diff(x) + 4*f(x),
        'sol': [Eq(f(x), C1*exp(x/2) + C2*exp(x*Rational(4, 3)))],
        'slow': True,
    },

    'lin_const_coeff_hom_06': {
        'eq': Eq(f(x).diff(x, 2) + 2*f(x).diff(x) - f(x), 0),
        'sol': [Eq(f(x), C1*exp(x*(-1 + sqrt(2))) + C2*exp(-x*(sqrt(2) + 1)))],
        'slow': True,
    },

    'lin_const_coeff_hom_07': {
        'eq': diff(f(x), x, 3) + diff(f(x), x, 2) - 10*diff(f(x), x) - 6*f(x),
        'sol': [Eq(f(x), C1*exp(3*x) + C3*exp(-x*(2 + sqrt(2))) + C2*exp(x*(-2 + sqrt(2))))],
        'slow': True,
    },

    'lin_const_coeff_hom_08': {
        'eq': f(x).diff(x, 4) - f(x).diff(x, 3) - 4*f(x).diff(x, 2) + \
        4*f(x).diff(x),
        'sol': [Eq(f(x), C1 + C2*exp(-2*x) + C3*exp(x) + C4*exp(2*x))],
        'slow': True,
    },

    'lin_const_coeff_hom_09': {
        'eq': f(x).diff(x, 4) + 4*f(x).diff(x, 3) + f(x).diff(x, 2) - \
        4*f(x).diff(x) - 2*f(x),
        'sol': [Eq(f(x), C3*exp(-x) + C4*exp(x) + (C1*exp(-sqrt(2)*x) + C2*exp(sqrt(2)*x))*exp(-2*x))],
        'slow': True,
    },

    'lin_const_coeff_hom_10': {
        'eq': f(x).diff(x, 4) - a**2*f(x),
        'sol': [Eq(f(x), C1*exp(-sqrt(a)*x) + C2*exp(sqrt(a)*x) + C3*sin(sqrt(a)*x) + C4*cos(sqrt(a)*x))],
        'slow': True,
    },

    'lin_const_coeff_hom_11': {
        'eq': f(x).diff(x, 2) - 2*k*f(x).diff(x) - 2*f(x),
        'sol': [Eq(f(x), C1*exp(x*(k - sqrt(k**2 + 2))) + C2*exp(x*(k + sqrt(k**2 + 2))))],
        'slow': True,
    },

    'lin_const_coeff_hom_12': {
        'eq': f(x).diff(x, 2) + 4*k*f(x).diff(x) - 12*k**2*f(x),
        'sol': [Eq(f(x), C1*exp(-6*k*x) + C2*exp(2*k*x))],
        'slow': True,
    },

    'lin_const_coeff_hom_13': {
        'eq': f(x).diff(x, 4),
        'sol': [Eq(f(x), C1 + C2*x + C3*x**2 + C4*x**3)],
        'slow': True,
    },

    'lin_const_coeff_hom_14': {
        'eq': f(x).diff(x, 2) + 4*f(x).diff(x) + 4*f(x),
        'sol': [Eq(f(x), (C1 + C2*x)*exp(-2*x))],
        'slow': True,
    },

    'lin_const_coeff_hom_15': {
        'eq': 3*f(x).diff(x, 3) + 5*f(x).diff(x, 2) + f(x).diff(x) - f(x),
        'sol': [Eq(f(x), (C1 + C2*x)*exp(-x) + C3*exp(x/3))],
        'slow': True,
    },

    'lin_const_coeff_hom_16': {
        'eq': f(x).diff(x, 3) - 6*f(x).diff(x, 2) + 12*f(x).diff(x) - 8*f(x),
        'sol': [Eq(f(x), (C1 + x*(C2 + C3*x))*exp(2*x))],
        'slow': True,
    },

    'lin_const_coeff_hom_17': {
        'eq': f(x).diff(x, 2) - 2*a*f(x).diff(x) + a**2*f(x),
        'sol': [Eq(f(x), (C1 + C2*x)*exp(a*x))],
        'slow': True,
    },

    'lin_const_coeff_hom_18': {
        'eq': f(x).diff(x, 4) + 3*f(x).diff(x, 3),
        'sol': [Eq(f(x), C1 + C2*x + C3*x**2 + C4*exp(-3*x))],
        'slow': True,
    },

    'lin_const_coeff_hom_19': {
        'eq': f(x).diff(x, 4) - 2*f(x).diff(x, 2),
        'sol': [Eq(f(x), C1 + C2*x + C3*exp(-sqrt(2)*x) + C4*exp(sqrt(2)*x))],
        'slow': True,
    },

    'lin_const_coeff_hom_20': {
        'eq': f(x).diff(x, 4) + 2*f(x).diff(x, 3) - 11*f(x).diff(x, 2) - \
        12*f(x).diff(x) + 36*f(x),
        'sol': [Eq(f(x), (C1 + C2*x)*exp(-3*x) + (C3 + C4*x)*exp(2*x))],
        'slow': True,
    },

    'lin_const_coeff_hom_21': {
        'eq': 36*f(x).diff(x, 4) - 37*f(x).diff(x, 2) + 4*f(x).diff(x) + 5*f(x),
        'sol': [Eq(f(x), C1*exp(-x) + C2*exp(-x/3) + C3*exp(x/2) + C4*exp(x*Rational(5, 6)))],
        'slow': True,
    },

    'lin_const_coeff_hom_22': {
        'eq': f(x).diff(x, 4) - 8*f(x).diff(x, 2) + 16*f(x),
        'sol': [Eq(f(x), (C1 + C2*x)*exp(-2*x) + (C3 + C4*x)*exp(2*x))],
        'slow': True,
    },

    'lin_const_coeff_hom_23': {
        'eq': f(x).diff(x, 2) - 2*f(x).diff(x) + 5*f(x),
        'sol': [Eq(f(x), (C1*sin(2*x) + C2*cos(2*x))*exp(x))],
        'slow': True,
    },

    'lin_const_coeff_hom_24': {
        'eq': f(x).diff(x, 2) - f(x).diff(x) + f(x),
        'sol': [Eq(f(x), (C1*sin(x*sqrt(3)/2) + C2*cos(x*sqrt(3)/2))*exp(x/2))],
        'slow': True,
    },

    'lin_const_coeff_hom_25': {
        'eq': f(x).diff(x, 4) + 5*f(x).diff(x, 2) + 6*f(x),
        'sol': [Eq(f(x),
        C1*sin(sqrt(2)*x) + C2*sin(sqrt(3)*x) + C3*cos(sqrt(2)*x) + C4*cos(sqrt(3)*x))],
        'slow': True,
    },

    'lin_const_coeff_hom_26': {
        'eq': f(x).diff(x, 2) - 4*f(x).diff(x) + 20*f(x),
        'sol': [Eq(f(x), (C1*sin(4*x) + C2*cos(4*x))*exp(2*x))],
        'slow': True,
    },

    'lin_const_coeff_hom_27': {
        'eq': f(x).diff(x, 4) + 4*f(x).diff(x, 2) + 4*f(x),
        'sol': [Eq(f(x), (C1 + C2*x)*sin(x*sqrt(2)) + (C3 + C4*x)*cos(x*sqrt(2)))],
        'slow': True,
    },

    'lin_const_coeff_hom_28': {
        'eq': f(x).diff(x, 3) + 8*f(x),
        'sol': [Eq(f(x), (C1*sin(x*sqrt(3)) + C2*cos(x*sqrt(3)))*exp(x) + C3*exp(-2*x))],
        'slow': True,
    },

    'lin_const_coeff_hom_29': {
        'eq': f(x).diff(x, 4) + 4*f(x).diff(x, 2),
        'sol': [Eq(f(x), C1 + C2*x + C3*sin(2*x) + C4*cos(2*x))],
        'slow': True,
    },

    'lin_const_coeff_hom_30': {
        'eq': f(x).diff(x, 5) + 2*f(x).diff(x, 3) + f(x).diff(x),
        'sol': [Eq(f(x), C1 + (C2 + C3*x)*sin(x) + (C4 + C5*x)*cos(x))],
        'slow': True,
    },

    'lin_const_coeff_hom_31': {
        'eq': f(x).diff(x, 4) + f(x).diff(x, 2) + f(x),
        'sol': [Eq(f(x), (C1*sin(sqrt(3)*x/2) + C2*cos(sqrt(3)*x/2))*exp(-x/2)
        + (C3*sin(sqrt(3)*x/2) + C4*cos(sqrt(3)*x/2))*exp(x/2))],
        'slow': True,
    },

    'lin_const_coeff_hom_32': {
        'eq': f(x).diff(x, 4) + 4*f(x).diff(x, 2) + f(x),
        'sol': [Eq(f(x), C1*sin(x*sqrt(-sqrt(3) + 2)) + C2*sin(x*sqrt(sqrt(3) + 2))
        + C3*cos(x*sqrt(-sqrt(3) + 2)) + C4*cos(x*sqrt(sqrt(3) + 2)))],
        'slow': True,
    },

    # One real root, two complex conjugate pairs
    'lin_const_coeff_hom_33': {
        'eq': f(x).diff(x, 5) + 11*f(x).diff(x) - 2*f(x),
        'sol': [Eq(f(x),
        C5*exp(r1*x) + exp(re(r2)*x) * (C1*sin(im(r2)*x) + C2*cos(im(r2)*x))
        + exp(re(r4)*x) * (C3*sin(im(r4)*x) + C4*cos(im(r4)*x)))],
        'checkodesol_XFAIL':True,  #It Hangs
    },

    # Three real roots, one complex conjugate pair
    'lin_const_coeff_hom_34': {
        'eq': f(x).diff(x,5) - 3*f(x).diff(x) + f(x),
        'sol': [Eq(f(x),
        C3*exp(r6*x) + C4*exp(r7*x) + C5*exp(r8*x)
        + exp(re(r9)*x) * (C1*sin(im(r9)*x) + C2*cos(im(r9)*x)))],
        'checkodesol_XFAIL':True, #It Hangs
    },

    # Five distinct real roots
    'lin_const_coeff_hom_35': {
        'eq': f(x).diff(x,5) - 100*f(x).diff(x,3) + 1000*f(x).diff(x) + f(x),
        'sol': [Eq(f(x), C1*exp(r11*x) + C2*exp(r12*x) + C3*exp(r13*x) + C4*exp(r14*x) + C5*exp(r15*x))],
        'checkodesol_XFAIL':True, #It Hangs
    },

    # Rational root and unsolvable quintic
    'lin_const_coeff_hom_36': {
        'eq': f(x).diff(x, 6) - 6*f(x).diff(x, 5) + 5*f(x).diff(x, 4) + 10*f(x).diff(x) - 50 * f(x),
        'sol': [Eq(f(x),
        C5*exp(5*x)
        + C6*exp(x*r16)
        + exp(re(r17)*x) * (C1*sin(im(r17)*x) + C2*cos(im(r17)*x))
        + exp(re(r19)*x) * (C3*sin(im(r19)*x) + C4*cos(im(r19)*x)))],
        'checkodesol_XFAIL':True, #It Hangs
    },

    # Five double roots (this is (x**5 - x + 1)**2)
    'lin_const_coeff_hom_37': {
        'eq': f(x).diff(x, 10) - 2*f(x).diff(x, 6) + 2*f(x).diff(x, 5)
        + f(x).diff(x, 2) - 2*f(x).diff(x, 1) + f(x),
        'sol': [Eq(f(x), (C1 + C2*x)*exp(x*r21) + (-((C3 + C4*x)*sin(x*im(r22)))
        + (C5 + C6*x)*cos(x*im(r22)))*exp(x*re(r22)) + (-((C7 + C8*x)*sin(x*im(r24)))
        + (C10*x + C9)*cos(x*im(r24)))*exp(x*re(r24)))],
        'checkodesol_XFAIL':True, #It Hangs
    },

    'lin_const_coeff_hom_38': {
        'eq': Eq(sqrt(2) * f(x).diff(x,x,x) + f(x).diff(x), 0),
        'sol': [Eq(f(x), C1 + C2*sin(2**Rational(3, 4)*x/2) + C3*cos(2**Rational(3, 4)*x/2))],
    },

    'lin_const_coeff_hom_39': {
        'eq': Eq(E * f(x).diff(x,x,x) + f(x).diff(x), 0),
        'sol': [Eq(f(x), C1 + C2*sin(x/sqrt(E)) + C3*cos(x/sqrt(E)))],
    },

    'lin_const_coeff_hom_40': {
        'eq': Eq(pi * f(x).diff(x,x,x) + f(x).diff(x), 0),
        'sol': [Eq(f(x), C1 + C2*sin(x/sqrt(pi)) + C3*cos(x/sqrt(pi)))],
    },

    'lin_const_coeff_hom_41': {
        'eq': Eq(I * f(x).diff(x,x,x) + f(x).diff(x), 0),
        'sol': [Eq(f(x), C1 + C2*exp(-sqrt(I)*x) + C3*exp(sqrt(I)*x))],
    },

    'lin_const_coeff_hom_42': {
        'eq': f(x).diff(x, x) + y*f(x),
        'sol': [Eq(f(x), C1*exp(-x*sqrt(-y)) + C2*exp(x*sqrt(-y)))],
    },

    'lin_const_coeff_hom_43': {
        'eq': Eq(9*f(x).diff(x, x) + f(x), 0),
        'sol': [Eq(f(x), C1*sin(x/3) + C2*cos(x/3))],
    },

    'lin_const_coeff_hom_44': {
        'eq': Eq(9*f(x).diff(x, x), f(x)),
        'sol': [Eq(f(x), C1*exp(-x/3) + C2*exp(x/3))],
    },

    'lin_const_coeff_hom_45': {
        'eq': Eq(f(x).diff(x, x) - 3*diff(f(x), x) + 2*f(x), 0),
        'sol': [Eq(f(x), (C1 + C2*exp(x))*exp(x))],
    },

    'lin_const_coeff_hom_46': {
        'eq': Eq(f(x).diff(x, x) - 4*diff(f(x), x) + 4*f(x), 0),
        'sol': [Eq(f(x), (C1 + C2*x)*exp(2*x))],
    },

    # Type: 2nd order, constant coefficients (two real equal roots)
    'lin_const_coeff_hom_47': {
        'eq': Eq(f(x).diff(x, x) + 2*diff(f(x), x) + 3*f(x), 0),
        'sol': [Eq(f(x), (C1*sin(x*sqrt(2)) + C2*cos(x*sqrt(2)))*exp(-x))],
    },

    #These were from issue: https://github.com/sympy/sympy/issues/6247
    'lin_const_coeff_hom_48': {
        'eq': f(x).diff(x, x) + 4*f(x),
        'sol': [Eq(f(x), C1*sin(2*x) + C2*cos(2*x))],
    },
    }
    }

