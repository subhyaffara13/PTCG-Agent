
def _get_examples_ode_sol_separable_reduced():
    df = f(x).diff(x)
    return {
            'hint': "separable_reduced",
            'func': f(x),
            'examples':{
    'separable_reduced_01': {
        'eq': x* df  + f(x)* (1 / (x**2*f(x) - 1)),
        'sol': [Eq(log(x**2*f(x))/3 + log(x**2*f(x) - Rational(3, 2))/6, C1 + log(x))],
        'simplify_flag': False,
        'XFAIL': ['lie_group'], #It hangs.
    },

    #Note: 'separable_reduced_02' is referred in 'separable_reduced_11'
    'separable_reduced_02': {
        'eq': f(x).diff(x) + (f(x) / (x**4*f(x) - x)),
        'sol': [Eq(log(x**3*f(x))/4 + log(x**3*f(x) - Rational(4,3))/12, C1 + log(x))],
        'simplify_flag': False,
        'checkodesol_XFAIL':True, #It hangs for this.
    },

    'separable_reduced_03': {
        'eq': x*df + f(x)*(x**2*f(x)),
        'sol': [Eq(log(x**2*f(x))/2 - log(x**2*f(x) - 2)/2, C1 + log(x))],
        'simplify_flag': False,
    },

    'separable_reduced_04': {
        'eq': Eq(f(x).diff(x) + f(x)/x * (1 + (x**(S(2)/3)*f(x))**2), 0),
        'sol': [Eq(-3*log(x**(S(2)/3)*f(x)) + 3*log(3*x**(S(4)/3)*f(x)**2 + 1)/2, C1 + log(x))],
        'simplify_flag': False,
    },

    'separable_reduced_05': {
        'eq': Eq(f(x).diff(x) + f(x)/x * (1 + (x*f(x))**2), 0),
        'sol': [Eq(f(x), -sqrt(2)*sqrt(1/(C1 + log(x)))/(2*x)),\
                   Eq(f(x), sqrt(2)*sqrt(1/(C1 + log(x)))/(2*x))],
    },

    'separable_reduced_06': {
        'eq': Eq(f(x).diff(x) + (x**4*f(x)**2 + x**2*f(x))*f(x)/(x*(x**6*f(x)**3 + x**4*f(x)**2)), 0),
        'sol': [Eq(f(x), C1 + 1/(2*x**2))],
    },

    'separable_reduced_07': {
        'eq': Eq(f(x).diff(x) + (f(x)**2)*f(x)/(x), 0),
        'sol': [
            Eq(f(x), -sqrt(2)*sqrt(1/(C1 + log(x)))/2),
            Eq(f(x), sqrt(2)*sqrt(1/(C1 + log(x)))/2)
        ],
    },

    'separable_reduced_08': {
        'eq': Eq(f(x).diff(x) + (f(x)+3)*f(x)/(x*(f(x)+2)), 0),
        'sol': [Eq(-log(f(x) + 3)/3 - 2*log(f(x))/3, C1 + log(x))],
        'simplify_flag': False,
        'XFAIL': ['lie_group'], #It hangs.
    },

    'separable_reduced_09': {
        'eq': Eq(f(x).diff(x) + (f(x)+3)*f(x)/x, 0),
        'sol': [Eq(f(x), 3/(C1*x**3 - 1))],
    },

    'separable_reduced_10': {
        'eq': Eq(f(x).diff(x) + (f(x)**2+f(x))*f(x)/(x), 0),
        'sol': [Eq(- log(x) - log(f(x) + 1) + log(f(x)) + 1/f(x), C1)],
        'XFAIL': ['lie_group'],#No algorithms are implemented to solve equation -C1 + x*(_y + 1)*exp(-1/_y)/_y

    },

    # Equivalent to example_name 'separable_reduced_02'. Only difference is testing with simplify=True
    'separable_reduced_11': {
        'eq': f(x).diff(x) + (f(x) / (x**4*f(x) - x)),
        'sol': [Eq(f(x), -sqrt(2)*sqrt(3*3**Rational(1,3)*(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3)
- 3*3**Rational(2,3)*exp(12*C1)/(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3) + 2/x**6)/6
- sqrt(2)*sqrt(-3*3**Rational(1,3)*(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3)
+ 3*3**Rational(2,3)*exp(12*C1)/(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3) + 4/x**6
- 4*sqrt(2)/(x**9*sqrt(3*3**Rational(1,3)*(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3)
- 3*3**Rational(2,3)*exp(12*C1)/(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3) + 2/x**6)))/6 + 1/(3*x**3)),
Eq(f(x), -sqrt(2)*sqrt(3*3**Rational(1,3)*(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3)
- 3*3**Rational(2,3)*exp(12*C1)/(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3) + 2/x**6)/6
+ sqrt(2)*sqrt(-3*3**Rational(1,3)*(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3)
+ 3*3**Rational(2,3)*exp(12*C1)/(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3) + 4/x**6
- 4*sqrt(2)/(x**9*sqrt(3*3**Rational(1,3)*(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3)
- 3*3**Rational(2,3)*exp(12*C1)/(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3) + 2/x**6)))/6 + 1/(3*x**3)),
Eq(f(x), sqrt(2)*sqrt(3*3**Rational(1,3)*(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3)
- 3*3**Rational(2,3)*exp(12*C1)/(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3) + 2/x**6)/6
- sqrt(2)*sqrt(-3*3**Rational(1,3)*(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3)
+ 3*3**Rational(2,3)*exp(12*C1)/(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3)
+ 4/x**6 + 4*sqrt(2)/(x**9*sqrt(3*3**Rational(1,3)*(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3)
- 3*3**Rational(2,3)*exp(12*C1)/(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3) + 2/x**6)))/6 + 1/(3*x**3)),
Eq(f(x), sqrt(2)*sqrt(3*3**Rational(1,3)*(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3)
- 3*3**Rational(2,3)*exp(12*C1)/(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3) + 2/x**6)/6
+ sqrt(2)*sqrt(-3*3**Rational(1,3)*(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3) + 3*3**Rational(2,3)*exp(12*C1)/(sqrt((3*exp(12*C1)
+ x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3) + 4/x**6 + 4*sqrt(2)/(x**9*sqrt(3*3**Rational(1,3)*(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1))
- exp(12*C1)/x**6)**Rational(1,3) - 3*3**Rational(2,3)*exp(12*C1)/(sqrt((3*exp(12*C1) + x**(-12))*exp(24*C1)) - exp(12*C1)/x**6)**Rational(1,3) + 2/x**6)))/6 + 1/(3*x**3))],
        'checkodesol_XFAIL':True, #It hangs for this.
        'slow': True,
    },

    #These were from issue: https://github.com/sympy/sympy/issues/6247
    'separable_reduced_12': {
        'eq': x**2*f(x)**2 + x*Derivative(f(x), x),
        'sol': [Eq(f(x), 2*C1/(C1*x**2 - 1))],
    },
    }
    }

